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
    "git status": "status",
    
    "download repository": "clone",
    "upload local branch commits remote": "push",
    "records file snapshots permanently version history": "commit",
    "set user name attach commit transactions": "config",
    "set user name globally": "config",
    "set user email globally": "config",
    "turn existing directory new git repository": "init",
    "updates current local working branch match remote": "pull",
    "condition current": "status",
    "show working directory status": "status",
    "switch different branch": "checkout",
    "create new branch": "branch",
    
    "help example commands": "help",
    "help": "help",
    "tutorial": "help",
}


def git_similarity(keywords):
    '''
    Compute the similarity between objects considering their representation as vectors.
    This function would compare two objects, and make a prediction of how similar they are.
    
        Parameters:
            keywords -- a list of strings to compare.
            
        Returns:
            command -- a string containing the most similar command.
    '''
    as_doc = " ".join(keywords)
    highest_sim = 0.0
    command = ""
    nlp = spacy.load('en_core_web_md')
    for key in git_commands.keys():
        current_sim = nlp(as_doc).similarity(nlp(key))
        if current_sim > highest_sim:
            highest_sim = current_sim
            command = git_commands[key]
    return command, highest_sim