import io

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from pandas import DataFrame
import matplotlib.pyplot as plt;plt.rcdefaults()
import numpy as np


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def index(request):
    return render(request, 'index.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        column_to_test = form.data['name']
        uploaded_file = form.files['data']

        bendfords_law_values = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
        percentages_of_leading_digits = get_digits_dist_from_data(column_to_test, uploaded_file)
        leading_digits = tuple(str(i) for i in range(1, 10))
        y_pos = np.arange(len(leading_digits))

        if percentages_of_leading_digits is not None:

            percentages_of_leading_digits = [round(elem, 1) for elem in percentages_of_leading_digits]

            x = np.arange(len(leading_digits))  # the label locations
            width = 0.45  # the width of the bars

            fig, ax = plt.subplots()
            actual = ax.bar(x - width / 2, percentages_of_leading_digits, width, label='Values from data')
            expected = ax.bar(x + width / 2, bendfords_law_values, width, label='Expected values from Benford\'s Law')
            ax.set_ylabel('Percentage occurrence of leading digit')
            if is_actual_close_to_expected(percentages_of_leading_digits, bendfords_law_values):
                ax.set_title('Benford\'s Law holds for ' + column_to_test)
            else:
                ax.set_title('Benford\'s Law does not hold for ' + column_to_test)
            ax.set_xticks(x)
            ax.set_xticklabels(leading_digits)
            ax.legend()

            autolabel(ax, actual)
            autolabel(ax, expected)

            fig.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='svg', bbox_inches='tight')
            svg = buf.getvalue()
            buf.close()
            plt.cla()
            return HttpResponse(svg, content_type='image/svg+xml')
        return HttpResponse("Invalid column selected")

    else:
        return HttpResponse("Not a POST method call")


def get_digits_dist_from_data(column, file):
    data = []

    for line in file:
        line_as_string = line.decode()
        if len(line_as_string) != 0:
            if line_as_string[-1] == '\n':
                line_as_string = line_as_string[:-1]
            data.append(line_as_string.split('\t'))

    dataframe = DataFrame(data[1:], columns=data[0])
    if column in dataframe.columns:
        count_of_leading_digit = {}
        column_data = dataframe[column].str[0]
        for i in range(1, 10):
            count_of_leading_digit[i] = column_data[column_data == str(i)].count()
        total_rows = column_data.count()
        percentages_of_leading_digits = [100 * count_of_leading_digit[i] / total_rows for i in range(1, 10)]
        return percentages_of_leading_digits
    return None


def is_actual_close_to_expected(actual, expected):
    for i in range(len(expected)):
        if actual[i] < expected[i] - 2 or actual[i] > expected[i] + 2:
            return False
    return True


def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
