from webgloss.factories import create_app

if __name__ == '__main__':
    app = create_app('webgloss.config.DevelopmentConfig')
    app.debug = True
    app.run()
