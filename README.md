Simple script that takes an index read and adds it to the end of the header of reads.
I used it after doing bcl2fastq for umi data.

Things to note:
make sure that nothing is removed based on quality in bcl2fastq.
In this example i used it on samples that had a I1 read of 8 bp and I2 of 10 bp
do it like this :


~~~~
bcl2fastq --runfolder-dir $1 -p 12 --output-dir $1/fastq_files \
--use-bases-mask Y*,I8,Y10,Y*  --minimum-trimmed-read-length 0 \
--mask-short-adapter-reads 0 --create-fastq-for-index-reads \
--no-lane-splitting
~~~~

this results in 4 output files: index one, read1 read2 and read3.
Index one is the one used for demulitplexing, while read 2 is the umi data.

i suggest renaming the data to read1 read2 and umi. (renaming read2 to umi and read3 to read2
, confusing i know)

i then use the script like this :

~~~~
python UMI2Header/U2H.py fix_barcode \
 --f1 read1.fastq.gz \
 --f2 read2.fastq.gz \
 --barcode umi.fastq.gz
 ~~~~

this results in an header to change from :
~~~~
@blaba:56:blabla:1:11101:10799:1082 3:N:0:AAGCCTAA
~~~~
to this: 
~~~~
@blaba:56:blabla:1:11101:10799:1082 3:N:0:AAGCCTAA_TACCTCCTGT
~~~~
this can then be aligned. i use bowtie2 with the "--sam-no-qname-trunc" so that the UMI tag
will make it to the bam file

deduplication can then be done with UMI_tools dedup (https://github.com/CGATOxford/UMI-tools)
