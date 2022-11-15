from pathlib import Path
from typing import Generator

from more_itertools import chunked
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from validate_email import return_blacklist, validate_email_fn


def main() -> None:
    path = Path('emails.txt')

    blacklist = return_blacklist()

    totalnlines = ncounter(path)

    with ThreadPoolExecutor() as executor:
        with tqdm(total=totalnlines, unit=" line(s)") as pbar:

            for chunk in return_chunks(path, chunk_size=totalnlines // 10):
                futures = {
                    executor.submit(worker, content, blacklist, pbar):
                    content
                    for content in chunk
                }
                results = set()
                for future in as_completed(futures):
                    results.add(future.result())

                for result in results:
                    print(result)

def worker(content: str, blacklist: set, bar: tqdm) -> tuple[bool, str]:

    email = content.strip()
    res = validate_email_fn(email, blacklist=blacklist)
    bar.update()
    return res, email


def return_chunks(path_to_file: Path,
                  chunk_size: int) -> Generator[list[str], None, None]:
    """
    Return chunks of lines of N size from a file
    ==================================
    """
    with open(path_to_file, errors='backslashreplace') as f:
        for chunk in chunked(f, chunk_size):
            yield chunk


def ncounter(path_to_file: Path, concurrency: bool = True) -> int:
    """
    Count all the lines in a file and return an int
    ===============================================
    uses the tqdm module to show progress if concurrency is set to False
    """
    ncount = 0
    if concurrency:
        with open(path_to_file, errors='backslashreplace') as f:
            ncount = sum(1 for _ in f)
        return ncount
    else:
        with tqdm(unit=" line(s)", desc="Counting lines") as ncounterbar:
            with open(path_to_file, errors='backslashreplace') as f:
                for _ in f:
                    ncount += 1
                    ncounterbar.update()
        return ncount


if __name__ == '__main__':
    main()