import spacy

git_commands = {
    "git add": "add",
    "git branch": "branch",
    "git checkout": "checkout",
    "git clone": "clone",
    "git commit -m": "commit",
    "git config --global username": "config",
    "git init": "init",
    "git pull": "pull",
    "git push": "push",
    "git status": "status"
}


def git_similarity(keywords):
    as_doc = " ".join(keywords)
    highest_sim = 0.0
    command = ""
    nlp = spacy.load('en_core_web_md')
    for key in git_commands.keys():
        current_sim = nlp(as_doc).similarity(nlp(key))
        if current_sim > highest_sim:
            highest_sim = current_sim
            command = git_commands[key]
    return command
