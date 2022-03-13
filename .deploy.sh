[ -z "$1" ] && echo "Need to specify version, exiting." && exit 1

echo "You are about to update to version ${1}. Please confirm upgrade with Y."

read confirmation
if [ $confirmation != "Y" ]
then
    echo No confirmation, exiting.
    exit
fi

python3 setup.py sdist
twine upload "dist/draftfast-${1}.tar.gz"

git tag $1
git push origin --tags