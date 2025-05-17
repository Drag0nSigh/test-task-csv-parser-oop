import argparse
import sys
from pathlib import Path
from typing import Dict, List, Union

sys.path.append(str(Path(__file__).parent.parent))

from scr.model.report import Payout
from scr.parsers.parsers import ParserCsv


class ValidateFilesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        valid_files = []
        for file_path in values:
            path = Path(file_path)
            # Проверяем существование файла
            if not path.exists():
                parser.error(f"Файл '{file_path}' не существует")
            # Проверяем, что это файл, а не директория
            if not path.is_file():
                parser.error(f"'{file_path}' не является файлом")
            # Проверяем расширение
            if path.suffix.lower() != '.csv':
                parser.error(f"Файл '{file_path}' должен иметь расширение "
                             f".csv")
            valid_files.append(file_path)
        setattr(namespace, self.dest, valid_files)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Обработка файлов и создание отчётов.'
    )
    parser.add_argument(
        'files',
        nargs='+',
        action=ValidateFilesAction,
        help='Пути к CSV-файлам для обработки (например, data1.csv data2.csv)'
    )
    parser.add_argument(
        '--report',
        required=True,
        choices=['payout_terminal', 'payout_json'],
        help='Тип отчёта: "payout_terminal" для вывода в терминал, '
             '"payout_json" для JSON'
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Имя выходного файла для отчёта (по умолчанию: output)'
    )
    return parser.parse_args()


def process_files(file_paths: List[str]) -> List[Dict[str, Union[str, int]]]:
    combined_result = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_text = file.read()
        except Exception as e:
            print(f'Ошибка при чтении файла "{file_path}": {e}')
            continue
        try:
            result = ParserCsv(csv_text).parser_data()
            combined_result += result
        except Exception as e:
            print(f'Ошибка при парсинге файла "{file_path}": {e}')
            continue
    if not combined_result:
        print('Ошибка: ни один файл не был успешно обработан.')
        sys.exit(1)
    return combined_result


def main():
    # Парсим аргументы командной строки
    args = parse_arguments()

    # Обрабатываем файлы
    combined_result = process_files(args.files)
    report = Payout(combined_result)

    # Выбираем тип отчёта
    if args.report == 'payout_terminal':
        report.payout_to_terminal()
    elif args.report == 'payout_json':
        script_dir = Path(__file__).parent.parent
        export_dir = script_dir / 'export'
        export_dir.mkdir(exist_ok=True)
        output_path = export_dir / f'{args.output}.json'
        report.payout_to_json(output_file=str(output_path))

    sys.exit()


if __name__ == '__main__':
    main()
