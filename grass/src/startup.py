from sources import startups


def startup(app):
    print('startup began')

    for startup_task in startups:
        app.send_task(startup_task.name)

    print('startup ended')
