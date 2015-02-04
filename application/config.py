
def config_update(app):
    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY='fafa#$#$F341G3322nfg3*rh2&b3r!fv',
        AES_PAD = '{',
        SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///hopping_mvp_db?instance=hopping-mvp:hopping-mvp-db',
        migration_directory= 'migrations',
        FACEBOOK_APP_ID = '1487715908166549',
        FACEBOOK_APP_SECRET = 'f0a263ef5a285e424fd8c34a85f148cd',
        COOKIE_NAME = 'hopp_cookie',
        SALT = 'as#2r92!B'
    ))

