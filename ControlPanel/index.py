__author__ = 'gokhankacan'
import flask, flask.views


app = flask.Flask(__name__)
app.secret_key = "FrEaKi"


@app.route('/')
def homepage():

    title = "Controle Panel HardMatch"

    try:
        return flask.render_template('index.html', title=title)
    except Exception as e:
        return str(e)

@app.errorhandler(404)
def page_not_found(e):

    title = "Pagina niet bekend"

    try:
        return flask.render_template('404.html', title=title)
    except Exception as e:
        return str(e)


def main():


    app.debug = True
    app.run()


if __name__ == "__main__": main()