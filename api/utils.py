import csv
import os
from io import StringIO

from fastapi.responses import StreamingResponse


def generate_and_save_csv(data, columns, filename, save_path="./reports"):
    """
    Gera um arquivo CSV, salva localmente e retorna uma resposta para download.

    :param data: Lista de objetos ou dicionários contendo os dados.
    :param columns: Lista de strings representando os nomes das colunas.
    :param filename: Nome do arquivo CSV a ser gerado.
    :param save_path: Caminho onde o arquivo será salvo localmente.
    :return: StreamingResponse contendo o arquivo CSV.
    """
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    for row in data:
        writer.writerow(row)
    output.seek(0)

    os.makedirs(save_path, exist_ok=True)
    local_file_path = os.path.join(save_path, filename)
    with open(local_file_path, "w", newline="") as file:
        file.write(output.getvalue())

    return StreamingResponse(
        StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
