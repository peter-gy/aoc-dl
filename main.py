from bs4 import BeautifulSoup
import requests
import pypandoc


def get_puzzle_url(year: int, day: int) -> str:
    base_url = 'https://adventofcode.com'
    return f'{base_url}/{year}/day/{day}'


def get_full_puzzle_html(year: int, day: int) -> str:
    puzzle_url = get_puzzle_url(year, day)
    response: requests.Response = requests.get(puzzle_url)
    if response.status_code != 200:
        raise RuntimeError(f'Bad response from GET({puzzle_url}). Status code: {response.status_code}')
    return response.text


def get_puzzle_description_html(year: int, day: int) -> str:
    full_html = get_full_puzzle_html(year, day)
    soup = BeautifulSoup(full_html, 'html.parser')
    description_html = soup.find('article', class_='day-desc')
    # spans may not be properly converted into markdown, so unwrap them and keep only their text content
    [span.unwrap() for span in description_html.find_all('span')]
    return description_html


def write_puzzle_description_to_md_file(year: int, day: int, basepath: str = ''):
    desc_html = get_puzzle_description_html(year, day)
    day_str = f'0{day}' if day < 10 else str(day)
    filename = f"puzzle-{year}-{day_str}.md"
    outputfile = f'{basepath}/{filename}' if basepath else filename
    pypandoc.convert_text(desc_html, 'md', format='html', outputfile=outputfile)


if __name__ == '__main__':
    write_puzzle_description_to_md_file(2019, 1)
