from flask import Flask, render_template, request, redirect, session
from Classes import *
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from Classes_projets_marchés_fi import *
matplotlib.use('Agg') #sinon error Run time loop in the main thread

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png')
    encoded = base64.b64encode(img.getvalue()).decode('utf-8')
    return ('data:image/png;base64,'+encoded)

def application_web(app):
    PT = ManagePtf()

    def collect_data(agents, simulation, tendance):
        modele = Simulation()
        modele.run(agents, simulation, tendance)
        modele.dashboard()
        modele.study_of_data()
        return modele.data_for_flask()

    @app.route('/', methods=('POST', 'GET'))
    def index():
        return render_template("index.html")




    """Projet Bloomberg"""
    @app.route('/projet_bloomberg', methods=('POST', 'GET'))
    def projet_bloomberg():
        refresh = False
        if request.method == 'POST':
            if request.form['submit_button'] == "Refresh":
                refresh = True

        date = ["27-01-2021", "16-02-2021"]
        sector = ["health_care", "utilities", "automobile", "bank", "chemical", "euro_stoxx600", "industrial", "technologies", "telecom"]
        fig, ptf = PT.projetChatronEvolution(refresh)
        plt.close(fig)
        image = fig_to_base64(fig)
        return render_template("projet_bloomberg.html", Sector = sector, Date = date, image=image, data=ptf.to_html())

    @app.route('/print_histo', methods=('POST', 'GET'))
    def print_histo():
        data = request.form.to_dict()
        try:
            session["sector"] = data["sector"]
            session["date"] = data["date"]
        except KeyError:
            pass
        else:
            session["sector"] = data["sector"]
            session["date"] = data["date"]

        data = PT.cleanDataChatron(session["date"],session["sector"])
        data_sector = PT.printDataSectorChatron()
        figure = PT.projetChatronPlotHisto()
        plt.close(figure)
        image = fig_to_base64(figure)
        return(render_template("print_histo.html", name = session["sector"], date=session["date"], data_sector = data_sector.to_html(), image = image, data = data.to_html()))


    @app.route('/print_best_firms', methods=('POST', 'GET'))
    def print_best_firms():
        if request.method == 'POST':
            try:
                data = request.form.to_dict()
                pe = float(data["pe"])
                peg_inf = float(data["peg_inf"])
                peg_sup = float(data["peg_sup"])
                ebit = float(data["ebit"])
                sharpe = float(data["sharpe"])
            except ValueError:
                return redirect(request.referrer)

            else:
                PT.cleanDataChatron(session["date"],session["sector"])
                match= PT.selectDataChatron(pe, peg_inf, peg_sup, ebit, sharpe)
                data = match.to_html()
                return(render_template('print_best_firms.html', Sector = session["sector"], data = data))




    """Projet Marchés fi"""
    @app.route('/index_marche_fi', methods=('POST', 'GET'))
    def index_marche_fi():
        trend = ["Baisse", "Hausse"]
        return render_template("index_marche_fi.html", tendance=trend)

    @app.route('/print_data', methods=('POST', 'GET'))
    def print_data():

        trend = ["Baisse", "Hausse"]

        # on récupère les données entrées par l'utilisateur
        if request.method == "POST":  # des données ont bien été rentrées
            values = request.form.to_dict()
        else:
            return render_template("index_marche_fi.html", tendance=trend)

        # cas où on n'a pas choisi un nombre d'agents et un nombre de simulations : on reste sur la page d'accueil
        try:
            agents = int(values["agent"])
            simulation = int(values["sim"])
        except ValueError:
            return render_template("index_marche_fi.html", tendance=trend)

        if values["trend"] == "Baisse":
            trend = 1
        else:
            trend = 0
        # on récupère les données
        df_strategies, df_best_strategies, list_ask, list_bid, list_pnl = collect_data(agents, simulation, trend)

        # on refait les graphiques pour ensuite les afficher
        fig = Figure()
        market = fig.add_subplot(1, 1, 1)
        market.set_title("Evolution du cours de l'action")
        market.set_xlabel("Iterations")
        market.set_ylabel("Prix en €")
        market.plot(np.linspace(0, 999, num=1000), list_bid, 'r', label='Bid')
        market.plot(np.linspace(0, 999, num=1000), list_ask, 'b', label='Ask')
        market.legend(title="Legend", loc="upper right", bbox_to_anchor=(1.08, 1))
        market.grid()

        fig2 = Figure()
        pnl = fig2.add_subplot(1, 1, 1)
        pnl.set_title("Evolution du cours des PnL")
        pnl.set_xlabel("Iterations")
        pnl.set_ylabel("€")
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[0], 'g', label='Careful Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[1], 'r', label='Clever Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[2], 'm', label='Passive Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[3], 'y', label='Normal Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[4], 'k', label='Short Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[5], 'b', label='Price Trader')
        pnl.legend(title="Legend", loc="upper right", bbox_to_anchor=(1.14, 1))
        pnl.grid()

        # On converti les graphiques en image sous format PNG
        pngImage = io.BytesIO()
        pngImage2 = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        FigureCanvas(fig2).print_png(pngImage2)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        pngImageB64String2 = "data:image/png;base64,"
        pngImageB64String2 += base64.b64encode(pngImage2.getvalue()).decode('utf8')

        # on affecte les variables au template
        template = render_template('print_data.html', image=pngImageB64String, image2=pngImageB64String2,
                                   data=df_strategies.to_html(), data_bis=df_best_strategies.to_html())
        return (template)

    if __name__ == "__main__":
        app.run(host='0.0.0.0')

app = Flask(__name__)
app.secret_key= "SimonLeBG22"
application_web(app)