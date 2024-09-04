# Academic impact of woc and woc-hack

This is an exercise in measuring academic impact of WoC and WocHack via citations. It can be applied in other cotexts as well.
We will use semanticscholar.org dataset to measure this impact. We have downloaded the dataset compressed json files on June 9 (i.e., papers and citations). 
It takes about 1TB of disk space. 

## Step 1
Identify semanicscholar IDs of core publications describing WoC 

```bash
zcat sematicscolar/papers-part*.jsonl.gz | grep -i 'world of c' | cut -d, -f1|cut -d: -f2 |sed 's|^|:|;s|$|,|' > woc
cat woc
:195298499,
:226222024,
```
We have two papers: in MSR and in International Journal of Empirical Software Engineering. 

## Step 2
Now get citations to these papers

```bash
zcat sematicscolar/citations-part*jsonl.gz| grep -Ff woc > woc.citations 
cat woc.citations | sed 's|.*"citingcorpusid":||;s|,"citedcorpusid":|;|;s|,.*||;s|;|:|;s|$|,|'|grep -Ff  woc | cut -d: -f1| sort -u   > woc1.citing
cat woc1.citing | sed 's|^|"corpusid":|;s|$|,|' > woc1.citing1
zcat sematicscolar/papers-part*.jsonl.gz | grep  -Ff woc1.citing1 > woc.citations.papers 
cat woc.citations.papers  | wc -l
103
```

We have 103 papers citing WoC core


## Step 3
Identify applications of WoC (WoC-Hack) papers.

We will look for papers that cite WoC core, and are produced by the core team and filter them to ensure they describe an application 
built using WoC.

First identify citing papers that have core-team author 
```bash
(python lst.py  | grep -i mockus |cut -d\; -f3 | sed 's|^|:|;s|$|,|'; cat woc) | sort -u > wocPlus
wc -l wocPlus
23
```
That yields 23 papers. We can go over titles and abstracts to confirm that each creates an application or a resources using WoC.

## Step 4
Now get citations to these papers

```bash
zcat sematicscolar/citations-part*jsonl.gz| grep -Ff wocPlus > wocPlus.citations 
cat wocPlus.citations | sed 's|.*"citingcorpusid":||;s|,"citedcorpusid":|;|;s|,.*||;s|;|:|;s|$|,|'|grep -Ff  wocPlus | cut -d: -f1| sort -u   > wocPlus1.citing
cat wocPlus1.citing | sed 's|^|"corpusid":|;s|$|,|' > wocPlus1.citing1
zcat sematicscolar/papers-part*.jsonl.gz | grep  -Ff wocPlus1.citing1 > wocPlus.citations.papers 
python lst.py wocPlus.citations.papers | grep -iv mockus | wc -l
208
```
We get 208 papers that cite these applications but are written by other research teams

## Step 5
Analyze these 208 papers citing woc-hack applications.

First separate self-citations papers that are 
```bash
python lst.py wocPlus.citations.papers | grep -i mockus | cut -d\; -f3 | sort -u | sed 's|^|:|;s|$|,|' > wocPlus.citations.papers.internal
sed 's|^|"citedcorpusid"|' wocPlus > a
sed 's|^|"citingcorpusid"|' wocPlus > b
sed 's|^|"citingcorpusid"|' wocPlus.citations.papers.internal > c
grep -Ff a wocPlus.citations | grep -Fvf b | grep -Fvf c | cut -d, -f 2 | sort -u | wc
208
```
Yes, the 208 papers are not self-citations

Now count influential (built on WoC-Hack) citations and methodology (using WoC-Hack) citations in this set of 208 papers. 
```bash
grep -Ff a wocPlus.citations | grep -Fvf b | grep -Fvf c | grep '"isinfluential":true'|wc
26
grep -Ff a wocPlus.citations | grep -Fvf b | grep -Fvf c | grep '"methodology"'|wc
96
```

Definitions:
"Semantic Scholar identifies citations where the cited publication has a significant impact on the citing publication, making it easier to understand how publications build upon and relate to each other. Influential citations are determined utilizing a machine-learning model analyzing a number of factors including the number of citations to a publication, and the surrounding context for each. You can read more about our approach in “Identifying Meaningful Citations”."
https://www.semanticscholar.org/paper/Identifying-Meaningful-Citations-Valenzuela-Ha/d5641d684df3a9e7c357923d109421fe4304ffa8

Citation intents make it easier for researchers to navigate and discover research while browsing our citation graph. We categorize citation intents into three different types; Background, Method and Result Extension.

    - Background citations provide historical context, justification of importance, and/or additional information directly related to that which exists in a cited paper.
    - Method citations use the previously established procedures or experiments to determine whether the results are consistent with findings in related studies.
    - Result citations extend on findings from research that was previously conducted.

Note: citation intent data is limited to papers for which we have access to the full text.
https://www.semanticscholar.org/paper/Structural-Scaffolds-for-Citation-Intent-in-Cohan-Ammar/99dd70ad75af11ce84098f58e5a9ae522cc73e3b




Out of 208 papers, 26 where wholly based on the WoC-Hack, while 96 used the methodology or data produced by WoC-Hack. 

## Pretty-printing results

```bash
python pretty.py woc.citations.papers > woc.bib
python pretty.py wocPlus.citations.papers > wocPlus.bib
```

