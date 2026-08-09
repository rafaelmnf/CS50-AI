# Finding the shortest path between any two actors by choosing a sequence of movies that connects them

import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        # transforma cada linha do arquivo CSV em um dicionário Python, onde as chaves são
        #  os cabeçalhos das colunas (ex: "id", "name", "birth")
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Pega o input da procurada e do target
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


# We can frame this as a search problem: our states are people. Our actions are movies, which take us from one actor to another 
# . Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can 
#  Return the shortest path from the person with id source to the person with the id target
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    if source == target:
        return []

    frontier = QueueFrontier()
    root = Node(source, None, None)
    frontier.add(root)

    explored = set()
    path = []
    
    while not frontier.empty():
        person = frontier.remove() # ao remover, no método já retorna a pessoa
        explored.add(person.state)
        # Retorna um set de tuplas {(movie_id, person_id), ...}
        relatedSet = neighbors_for_person(person.state) # Procura os vizinhos e cria um Set para deles
        # Adiciona todos os vizinhos na fila da fronteira
        for movie_id, person_id in relatedSet:
            # Cria o um nó para a add na fronteira contendo o id = state, no pai = parent e action = movie
            node = Node(person_id, person, movie_id)
            # Verificar se o nó já não está no explored
            if node.state not in explored:
                # Se um dos nós vizinhos forem o target, vai voltando para cada parent e salvando o movie e o id da pessoa atual até chegar na root
                if node.state == target:
                    while node.state != source: 
                        path.append((node.action, node.state))
                        node = node.parent
                    path.reverse()
                    return path
                frontier.add(node)

    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
