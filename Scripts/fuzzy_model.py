from thefuzz import process

choices = [
    # git basic commands
    'git',
    'add',
    'branch',
    'checkout',
    'clone',
    'commit',
    'config',
    'init',
    'pull',
    'push',
    'status',
    
    # verb
    'setup',
    'create',
    'set',
    'upload',
    'download',
    'records',
    'turn',
    'match',
    'update',
    'show',
    'turn',
    
    'local',
    'remote',
    'repository',
    'snapshots',
    'version',
    'control',
    'history',
    'existing',
    'directory',
    'working',
    'navigate',
    'switch',
    'different',
    'new',
    'file',
    'current',
    'globally',
    'branch',
    'condition',
    
    'help',
    'example',
    'commands',
    'tutorial',
    
    # add any other generic word you want
]

def fuzzy_match(keywords):
    ''' 
    Compute the similarity between sequences of characters using Levenshtein distance.
    This function would filter out typos, plural, and other variations, 
    into one generic word of choice.
    
        Parameters:
            keywords -- a list of strings to compare.
        
        Returns:
            res -- a list containing a single match of each keyword.
    '''
    res = []
    for word in keywords:
        (match, score) = process.extractOne(word, choices)
        res.append(match)
    return res

if __name__ == '__main__':
    '''
    To test it out, run this script in the terminal:
    '''
    keywords = ['setp', 'pushes', 'pulled', 'initializedddd']
    print(fuzzy_match(keywords))
    # expected output: ['setup', 'push', 'pull', 'init']