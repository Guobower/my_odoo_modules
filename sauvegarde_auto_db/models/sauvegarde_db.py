from odoo import models, fields, api, tools, _
from odoo.exceptions import Warning
import odoo
from odoo.http import content_disposition

import logging

_logger = logging.getLogger(__name__)
from ftplib import FTP
import os
import datetime

try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib
import time
import base64
import socket


def execute(connector, method, *args):
    res = False
    try:
        res = getattr(connector, method)(*args)
    except socket.error as error:
        _logger.critical('Error while executing the method "execute". Error: ' + str(error))
        raise error
    return res


class sauvegarde_db(models.Model):
    _name = 'sauvegarde.db'

    @api.multi
    def get_db_list(self, host, port, context={}):
        uri = 'http://' + host + ':' + port
        conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
        db_list = execute(conn, 'list')
        return db_list

    @api.multi
    def _get_db_name(self):
        dbName = self._cr.dbname
        return dbName

    @api.multi
    def _check_db_exist(self):
        self.ensure_one()

        db_list = self.get_db_list(self.host, self.port)
        if self.name in db_list:
            return True
        return False

    _constraints = [(_check_db_exist, _('Error ! No such database exists!'), [])]

    # Columns for local server configuration
    host = fields.Char('Host', required=True, default='localhost')
    port = fields.Char('Port', required=True, default=8069)
    name = fields.Char('Database', required=True, help='Database you want to schedule backups for',
                       default=_get_db_name)
    folder = fields.Char('Backup Directory', help='Absolute path for storing the backups', required='True',
                         default='/odoo/new/backups')
    backup_type = fields.Selection([('zip', 'Zip'), ('dump', 'Dump')], 'Backup Type', required=True, default='zip')
    autoremove = fields.Boolean('Auto. Remove Backups',
                                # help='If you check this option you can choose to automaticly remove the backup after xx days')
                                help='Si cette option est cochée vous devez choisir le  to automaticly remove the backup after xx days')
    days_to_keep = fields.Integer('Remove after x days',
                                  help="Choose after how many days the backup should be deleted. For example:\nIf you fill in 5 the backups will be removed after 5 days.",
                                  required=True)

    @api.model
    def schedule_backup(self):
        conf_ids = self.search([])

        for rec in conf_ids:
            db_list = self.get_db_list(rec.host, rec.port)

            if rec.name in db_list:
                try:
                    if not os.path.isdir(rec.folder):
                        os.makedirs(rec.folder)
                except:
                    raise
                # Create name for dumpfile.
                bkp_file = '%s_%s.%s' % (time.strftime('%Y_%m_%d_%H_%M_%S'), rec.name, rec.backup_type)
                file_path = os.path.join(rec.folder, bkp_file)
                uri = 'http://' + rec.host + ':' + rec.port
                conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
                bkp = ''
                try:
                    # try to backup database and write it away
                    fp = open(file_path, 'wb')
                    odoo.service.db.dump_db(rec.name, fp, rec.backup_type)
                    fp.close()
                except Exception as error:
                    _logger.debug(
                        "Couldn't backup database %s. Bad database administrator password for server running at http://%s:%s" % (
                            rec.name, rec.host, rec.port))
                    _logger.debug("Exact error from the exception: " + str(error))
                    continue

            else:
                _logger.debug("database %s doesn't exist on http://%s:%s" % (rec.name, rec.host, rec.port))

            """
            Remove all old files (on local server) in case this is configured..
            """
            if rec.autoremove:
                dir = rec.folder
                # Loop over all files in the directory.
                for f in os.listdir(dir):
                    fullpath = os.path.join(dir, f)
                    # Only delete the ones wich are from the current database
                    # (Makes it possible to save different databases in the same folder)
                    if rec.name in fullpath:
                        timestamp = os.stat(fullpath).st_ctime
                        createtime = datetime.datetime.fromtimestamp(timestamp)
                        now = datetime.datetime.now()
                        delta = now - createtime
                        if delta.days >= rec.days_to_keep:
                            # Only delete files (which are .dump and .zip), no directories.
                            if os.path.isfile(fullpath) and (".dump" in f or '.zip' in f):
                                _logger.info("Delete local out-of-date file: " + fullpath)
                                os.remove(fullpath)
