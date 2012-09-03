from flask import Flask
from flask import request, redirect, url_for

app = Flask(__name__)

# This lets me change what I redirect to from my "homepage" (caleb.pythonanywhere.com).
@app.route('/')
def index():
    return redirect(url_for('net_worth_page'))

@app.route('/net_worth_page', methods=['GET', 'POST'])
def net_worth_page():
    if request.method == "GET":
        return generate_form()
    else:
        income = int(request.form['income'])
        expenses = int(request.form['expenses'])
        start_year = int(request.form['startyear'])
        years = int(request.form['years'])

        year_list = generate_year_list(start_year, years)
        net_worth = generate_net_worth(income, expenses, years)

        return generate_graph(year_list, net_worth, "Net Worth")

def generate_net_worth(income, expenses, number_years):
    projection = []
    total = 0
    for year in range(number_years):
        total = total + (income - expenses)
        projection.append(total)
    return projection

def generate_year_list(start_year, number_years):
    return range(start_year, start_year+number_years+1)

def generate_form():
    return """
            <form action="/net_worth_page" method="POST">
                Yearly Income <input type="text" name="income" /> <br />
                Yearly Expenses <input type="text" name="expenses" /> <br />
                Start Year <input type="text" name="startyear" /> <br />
                Years to Project <input type="text" name="years" /> <br />
                <input type="submit" />
            </form>
        """

def generate_graph(x_axis, y_axis, title=''):
    return """
    <html><head>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        <script type="text/javascript">
            $(function () {
                var chart;
                $(document).ready(function() {
                    chart = new Highcharts.Chart({
                        chart: {
                            renderTo: 'container',
                            type: 'line',
                            marginRight: 130,
                            marginBottom: 100
                        },
                        title: {
                            text: '%(title)s',
                            x: -20 //center
                        },
                        subtitle: {
                            text: '',
                            x: -20
                        },
                        xAxis: {
                            categories: %(x_axis)s,
                            labels: {
                                rotation: -45,
                                align: 'right'
                            }
                        },
                        yAxis: {
                            title: {
                                text: 'Dollars'
                            },
                            plotLines: [{
                                value: 0,
                                width: 1,
                                color: '#808080'
                            }]
                        },
                        tooltip: {
                            formatter: function() {
                                    return '<b>'+ this.series.name +'</b><br/>'+
                                    this.x +': '+ this.y;
                            }
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'top',
                            x: -10,
                            y: 100,
                            borderWidth: 0
                        },
                        series: [{
                            name: 'Net Worth',
                            data: %(y_axis)s
                        }]
                    });
                });

            });
        </script>
    </head><body>
    <script src="http://test.calebmadrigal.com/jshost/highcharts/highcharts.js"></script>
    <script src="http://test.calebmadrigal.com/jshost/highcharts/modules/exporting.js"></script>

    <div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>
    </body></html>
    """ % {'x_axis': str(x_axis), 'y_axis': str(y_axis), 'title': title }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9070)