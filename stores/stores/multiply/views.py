from django.http import HttpResponse


def multiply_table(request):
    table = "\t\t\t\tТаблица умножения от 1 до 10\n"


    for i in range(1, 11):
        table += f"\n\t\t\t\tТаблица умножения на {i}:\n"

        for j in range(1, 11):
            result = i * j
            table += f"\t\t\t\t{i} × {j:2} = {result:3}\n"
        table += "\n"


    return HttpResponse(f"<pre>{table}</pre>")
