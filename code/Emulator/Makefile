TESTS=pyemu

test:
	bin/test ${TESTS} \
		--with-coverage --cover-package="${TESTS}" \
		--cover-erase --cover-html --cover-html-dir=var/html

buildout:
	bin/buildout -v

gui:
	bin/pyemu gui apps/pyemu/pyemu/test/test_program_1

run:
	bin/pyemu apps/pyemu/pyemu/test/test_program_1
