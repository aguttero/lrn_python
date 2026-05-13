## Tutorial YouTube Links
Net Nija
https://www.youtube.com/watch?v=QV0kVNvkMxc

## Lista de comandos

# Local init + first commit
	Git init
	Git add .
	Git commit -m “message present tense”

# Connect to GitHub
    Create a GitHub Repo
    Create a local init
    Commit local inital commit
    Execute commands in GitHub repo screen
    git remote add origin <github repo URI>
    git push -u origin main

# Clone GitHub repo
    git clone <github repo uri>


# Borrar files de stage o repo
	Git rm —cached <filename> para sacar file de stage
	Git rm — cached -r . -> todos los files del directorio ‘.’
	Git restore --staged <file>..." to unstage
    Agregar a .gitignore para que no vuelva a subir

# Limpar commits erroneos
    Borrar repo github
    retroceder n commits locales
        git reset --soft HEAD~n
    crear nuevo commit limpio
        git commit -m "version limpia codebase"
    limpiar otras ramas si es necesario
        git checkout <branch name>
        git reset --soft HEAD~n
        git commit -m "version limpia codebase branchname"
    forzar subida de GitHub
        git push origin main --force


# Eliminar local git tracking
    rm -rf .git    

# Status
    git status
    git log [--oneline]

# Branching
    Create:
        git branch <new branch name>
        git checkout -b <new branch name>
    
    List:   git branch -a
    Switch: git checkout <branch name>
    Commit: as always
    push: git push origin <branch name> -u [la primeravez]

    Delete: cambiar a main
            git branch -d (post merge) / -D (fuerza delete) <branch name>

    Delete remote: git push origin --delete <nombre-de-la-rama>

    If Github does not allow to delete the remote feature branch:
        - Check if GitHub has it configured as Default Branch
        Solution:
            Go Repo in GitHub
            Click Settings
            Select Branches in the left nav bar
            In Default Branch section click icon 'Swithc to another branch'
            Choose a different branch than the one to be deleted
            Click Update
            Confirm if requested
            Retry CLI git push origin --delete <nombre-de-la-rama>


## Merge:
    Merge:  ir a la branch en la que se quieren recibir los cambios
            git checkout main
            git merge <branch name (feature-a)>

## Merge Conflicts: Example git .gitignore conflict file:
    1. identify the conflict
        Run git status to see the conflicted files.
        The conflicted file(s) will appear under "Unmerged paths".
    2. Open the file
        Open .gitignore in your text editor.
        Locate the Git conflict markers:
            * <<<<<<< HEAD: Changes from your current branch (main).
            * =======: The dividing line between the two versions.
            * >>>>>>> feature-branch: Changes from the incoming branch.

    3. Edit the Contents
        Decide which block patterns you need to keep.
        Usually, you want to keep lines from both branches.
        Delete the conflict markers completely (<<<<<<<, =======, >>>>>>>).
        Rearrange the remaining rules into clean, logical sections. [9, 10, 11, 12, 13] 
    
    4 Example Resolution
        Conflicted File:
            <<<<<<< HEAD
            /node_modules
            /.env
            =======
            /node_modules
            /dist
            >>>>>>> feature-branch

        Resolved File:
            /node_modules
            /.env
            /dist

    4 Stage and Commit
        Save the edited file.
        Run git add .gitignore to mark the conflict as resolved.
        Run git commit -m "Merge branch 'feature-branch' and resolve .gitignore conflict" to complete the merge. 






