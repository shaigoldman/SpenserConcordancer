for i in {1..6}
do
	echo "loading book $i"
	lynx -dump https://www.luminarium.org/renascence-editions/queene$i.html > resources/queene$i.txt	
done
