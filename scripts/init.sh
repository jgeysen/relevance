echo "-> initialise git repo"
git init

echo "-> running pipenv install --dev" \
&& pipenv install --dev \
&& echo "-> installed developer environment <-"

echo "-> set git to follow tags on push"
git config push.followTags true

echo "-> configure git hooks"
pre-commit install -t pre-commit
pre-commit install -t pre-push

echo "-> creating initial commit in master" \
&& git add . \
&& git commit -m "initial commit" --no-verify \
&& (
	git remote add origin git@github.com:anmut-consulting/relevance.git \
	|| echo "WARNING: problem with remote.  Please verify.") \
&& echo "Creating 'latest' tag" \
&& git tag -f latest \
&& git push -u origin master --no-verify --tags \
&& echo "  -> adding dev branch" \
&& git checkout -b dev \
&& git push -u origin dev

echo "Creating ipython kernel for use with Jupyter"
pipenv run create_ipykernel

echo
echo "#################################################"
echo "REPO FULLY INITIALISED! You're set up to develop."
echo "#################################################"
