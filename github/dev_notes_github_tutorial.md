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

    Delte remote: git push origin --delete <nombre-de-la-rama>

    Merge:  ir a la branch en la que se quieren recibir los cambios
            git checkout main
            git merge branch name (feature-a)








