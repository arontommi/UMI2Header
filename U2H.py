import os
import gzip
import fire
from subprocess import call

class Umi2Header(object):
    """input fastqfiles"""

    def fq(self, filename):
        if filename.endswith('.gz'):
            fastq = gzip.open(filename, 'rb')
        else:
            fastq = open(filename, 'rb')
        with fastq as f:
            while True:
                l1 = f.readline()
                if not l1:
                    break
                l2 = f.readline()
                l3 = f.readline()
                l4 = f.readline()
                read = [l1, l2, l3, l4]
                yield read

    def gzip_suproccess(self, file):
        "since python gzip takes for ever"
        path = os.getcwd() + '/'
        pathfile = path + file
        call(['gzip', '{}'.format(pathfile)])

    def remove_previous_umi(self,file):
        path = os.getcwd() + '/'
        if os.path.isfile(path + file.split('.')[0] + '.UMI.fastq.gz'):
            os.remove(path + file.split('.')[0] + '.UMI.fastq.gz')
        else:
            pass

    def fix_barcode(self, f1, f2, barcode):
        self.remove_previous_umi(f1)
        self.remove_previous_umi(f2)
        filename1 = f1.split('.')[0] + '.UMI.fastq'
        filename2 = f2.split('.')[0] + '.UMI.fastq'
        file1 = open(filename1, "ab")
        file2 = open(filename2, "ab")

        for r1, r2, r3 in zip(self.fq(f1), self.fq(f2), self.fq(barcode)):
            file1.writelines([r1[0].rstrip() + b"_" + r3[1],
                              r1[1],
                              r1[2],
                              r1[3]])
            file2.writelines([r2[0].rstrip() + b"_" + r3[1],
                              r2[1],
                              r2[2],
                              r2[3]])
        file1.close()
        file2.close()
        self.gzip_suproccess(filename1)
        self.gzip_suproccess(filename2)


def main():
   fire.Fire(Umi2Header)


if __name__ == '__main__':
    main()
