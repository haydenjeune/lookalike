import connexion


def ping():
    return "pong"

    import connexion


app = connexion.FlaskApp(__name__)
app.add_api("spec.yaml")
app.run(port=8080)