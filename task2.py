import concurrent.futures
from collections import defaultdict
from multiprocessing import Queue, Process

def find_in_file(args):
    for jq, file_name, words in args:
        with open(file_name) as file:
            content = file.read()

            for word in words:
                if word in content:
                    jq.put((word, file_name))

def chunks(files, max_workers):
    per_chunk = len(files) // max_workers

    for i in range(0, len(files), per_chunk):
        yield files[i:i + per_chunk]

def main(files: list, words: list, max_workers = 2):
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        result = {}
        for word in words:
            result[word] = set()


        jq = Queue()

        args = list(chunks([(jq, file_name, words) for file_name in files], max_workers))

        processes = []

        for i in range(max_workers+1):
            process = Process(target=find_in_file, args=(args[i],))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()


        while not jq.empty():
            word, file_name = jq.get()

            result[word].add(file_name)

        return result


if __name__ == "__main__":
    files = [
        'league_lore_story_1.txt',
        'league_lore_story_2.txt',
        'league_lore_story_3.txt',
        'league_lore_story_4.txt',
        'league_lore_story_5.txt',
    ]

    print(main(files, ['Demacia', 'Malzahar', 'kingdom', 'was']))