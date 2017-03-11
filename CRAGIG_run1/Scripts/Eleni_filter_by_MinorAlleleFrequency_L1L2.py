### Eleni Petrou
### June 15, 2015
### This script takes an input haplotype file with loci in rows and individuals in columns and calculated the allele frequencies for each allele at
### each locus. This script is based on Charlie's MAF_corrected_gebotypes script
#cd /mnt/hgfs/D/sequencing_data/Herring_PopulationStructure/output_stacks
#python Eleni_filter_by_MinorAlleleFrequency.py CORRECTED_TRANSPOSED_GENOTYPES

## NL edited for CRAGIG Run1


import sys

# Open your files for reading and writing
genotypes_file = open(sys.argv[1],'r')
output_freqs = open("batch_100_filteredMAF_outputFreqs",'w')
filtered_genotypes = open("batch_100_filteredMAF_genotypes.csv",'w')
blacklisted_genotypes = open("batch_100_filteredMAF_BADgenotypes.csv" ,'w')
blacklisted_MAF = open("batch100_blacklistedMAF.csv",'w')

# Tell the computer that your files have headers
header = True

# This code creates a list of each allele for each population. This will be the headers for the file that outputs the allele frequencies. Modify as needed.
MAF_header = str("Locus" + '\t' +
"Allele1_Pohang" + '\t' + "Allele2_Pohang" + '\t' +
"Allele1_Geoje15" + '\t' + "Allele2_Geoje15" + '\t' +
"Allele1_Namhae" + '\t' + "Allele2_Namhae"+ '\t' +
"Allele1_YellowSea" + '\t' + "Allele2_YellowSea" + '\t' +
"Allele1_Boryeong" + '\t' + "Allele2_Boryeong" + '\t' +
"Allele1_Geoje14" + '\t' + "Allele2_Geoje14" + '\t' +
"Allele1_SocMuk" + '\t' + "Allele2_SocMuk")
output_freqs.write(MAF_header + '\n')
blacklisted_MAF.write(MAF_header + '\n')



for mystring in genotypes_file:							# Read in each line in the file as a string
	if header:											# This code takes the header from the original genotypes file and saves it as the header of the output genotypes files. We do not remove any individuals in this script so we can keep the original headers
		genotypes_header = mystring
		filtered_genotypes.write(genotypes_header)
		blacklisted_genotypes.write(genotypes_header)
		header = False
	else:
		#print mystring
		stripped_string = mystring.strip('\n')					## Make sure to strip your string of the newline, otherwise weird stuff might happen.
		locus = stripped_string.split(",")[0] 					## This tells the computer how to split your string. If csv, use comma. This saves the locus name.
		locus_freqs = []
		bad_locus_freqs = []
		#print locus
		# Specifying which individuals belong in each population
		# Rule = [excel column -1 : excel column]
		### BE VERY CAREFUL!!Change column indices to fit your file . IF csv, specify comma use. This saves the genotypes associated with each locus. Remember arguments start at 0 .GOES UP TO BUT NOT INCLUDING SEVEN!!!
		Pohang = stripped_string.split(",")[1:28]
		Geoje15 = stripped_string.split(",")[28:61]
		Namhae = stripped_string.split(",")[62:77]
		YellowSea = stripped_string.split(",")[78:84]
		Boryeong = stripped_string.split(",")[85:87]
		Geoje14 = stripped_string.split(",")[88:120]
		SocMuk = stripped_string.split(",")[121:132]


		###CHECK THIS OUTPUT TO MAKE SURE YOU DID NOT FUCK UP!!

		## Counting occurrences of hets and homos in each population

		CountOf_homo1_Pohang = float(Pohang.count("0101"))
		CountOf_homo2_Pohang = float(Pohang.count("0202"))
		CountOf_het_Pohang = float(Pohang.count("0102"))
		#print CountOf_homo1_Geoje15

		CountOf_homo1_Geoje15 = float(Geoje15.count("0101"))
		CountOf_homo2_Geoje15 = float(Geoje15.count("0202"))
		CountOf_het_Geoje15 = float(Geoje15.count("0102"))

		CountOf_homo1_Namhae = float(Namhae.count("0101"))
		CountOf_homo2_Namhae = float(Namhae.count("0202"))
		CountOf_het_Namhae = float(Namhae.count("0102"))

		CountOf_homo1_YellowSea = float(YellowSea.count("0101"))
		CountOf_homo2_YellowSea = float(YellowSea.count("0202"))
		CountOf_het_YellowSea = float(YellowSea.count("0102"))

		CountOf_homo1_Boryeong = float(Boryeong.count("0101"))
		CountOf_homo2_Boryeong = float(Boryeong.count("0202"))
		CountOf_het_Boryeong = float(Boryeong.count("0102"))

		CountOf_homo1_Geoje14 = float(Geoje14.count("0101"))
		CountOf_homo2_Geoje14 = float(Geoje14.count("0202"))
		CountOf_het_Geoje14 = float(Geoje14.count("0102"))

		CountOf_homo1_SocMuk = float(SocMuk.count("0101"))
		CountOf_homo2_SocMuk = float(SocMuk.count("0202"))
		CountOf_het_SocMuk = float(SocMuk.count("0102"))

		# Calculating allele frequencies for each population.  Add 0.00001 so you don't divide by zero.
		total_alleles_Pohang=2*(CountOf_homo1_Pohang + CountOf_homo2_Pohang + CountOf_het_Pohang + 0.000000001)
		FrequencyOf_allele1_Pohang = ((2 * CountOf_homo1_Pohang) + (CountOf_het_Pohang)) / (total_alleles_Pohang)
		FrequencyOf_allele2_Pohang = ((2 * CountOf_homo2_Pohang) + (CountOf_het_Pohang)) / (total_alleles_Pohang)

		total_alleles_Geoje15=2*(CountOf_homo1_Geoje15 + CountOf_homo2_Geoje15 + CountOf_het_Geoje15 + 0.000000001)
		FrequencyOf_allele1_Geoje15 = ((2 * CountOf_homo1_Geoje15) + (CountOf_het_Geoje15)) / (total_alleles_Geoje15)
		FrequencyOf_allele2_Geoje15 = ((2 * CountOf_homo2_Geoje15) + (CountOf_het_Geoje15)) / (total_alleles_Geoje15)

		total_alleles_Namhae=2*(CountOf_homo1_Namhae + CountOf_homo2_Namhae + CountOf_het_Namhae + 0.000000001)
		FrequencyOf_allele1_Namhae = ((2 * CountOf_homo1_Namhae) + (CountOf_het_Namhae)) / (total_alleles_Namhae)
		FrequencyOf_allele2_Namhae = ((2 * CountOf_homo2_Namhae) + (CountOf_het_Namhae)) / (total_alleles_Namhae)

		total_alleles_YellowSea=2*(CountOf_homo1_YellowSea + CountOf_homo2_YellowSea + CountOf_het_YellowSea + 0.000000001)
		FrequencyOf_allele1_YellowSea = ((2 * CountOf_homo1_YellowSea) + (CountOf_het_YellowSea)) / (total_alleles_YellowSea)
		FrequencyOf_allele2_YellowSea = ((2 * CountOf_homo2_YellowSea) + (CountOf_het_YellowSea)) / (total_alleles_YellowSea)

		total_alleles_Boryeong=2*(CountOf_homo1_Boryeong + CountOf_homo2_Boryeong + CountOf_het_Boryeong + 0.000000001)
		FrequencyOf_allele1_Boryeong = ((2 * CountOf_homo1_Boryeong) + (CountOf_het_Boryeong)) / (total_alleles_Boryeong)
		FrequencyOf_allele2_Boryeong = ((2 * CountOf_homo2_Boryeong) + (CountOf_het_Boryeong)) / (total_alleles_Boryeong)

		total_alleles_Geoje14=2*(CountOf_homo1_Geoje14 + CountOf_homo2_Geoje14 + CountOf_het_Geoje14 + 0.000000001)
		FrequencyOf_allele1_Geoje14 = ((2 * CountOf_homo1_Geoje14) + (CountOf_het_Geoje14)) / (total_alleles_Geoje14)
		FrequencyOf_allele2_Geoje14 = ((2 * CountOf_homo2_Geoje14) + (CountOf_het_Geoje14)) / (total_alleles_Geoje14)

		total_alleles_SocMuk=2*(CountOf_homo1_SocMuk + CountOf_homo2_SocMuk + CountOf_het_SocMuk + 0.000000001)
		FrequencyOf_allele1_SocMuk = ((2 * CountOf_homo1_SocMuk) + (CountOf_het_SocMuk)) / (total_alleles_SocMuk)
		FrequencyOf_allele2_SocMuk = ((2 * CountOf_homo2_SocMuk) + (CountOf_het_SocMuk)) / (total_alleles_SocMuk)


		if ((FrequencyOf_allele1_Pohang >= 0.05) or (FrequencyOf_allele1_Geoje15 >= 0.05) \
			or (FrequencyOf_allele1_Namhae >= 0.05) or (FrequencyOf_allele1_YellowSea >= 0.05) \
			or (FrequencyOf_allele1_Boryeong >= 0.05) or (FrequencyOf_allele1_Geoje14 >= 0.05) or (FrequencyOf_allele1_SocMuk >= 0.05))\
			and ((FrequencyOf_allele2_Pohang >= 0.05) or (FrequencyOf_allele2_Geoje15 >= 0.05) \
			or (FrequencyOf_allele2_Namhae >= 0.05) or (FrequencyOf_allele2_YellowSea >= 0.05) \
			or (FrequencyOf_allele2_Boryeong >= 0.05) or (FrequencyOf_allele2_Geoje14 >= 0.05) or (FrequencyOf_allele2_SocMuk >=
			0.05)):

			locus_freqs.append(locus+'\t'+
			str(FrequencyOf_allele1_Geoje15) + '\t' + str(FrequencyOf_allele2_Geoje15) + '\t' +
			str(FrequencyOf_allele1_Boryeong) + '\t' + str(FrequencyOf_allele2_Boryeong) + '\t' +
			str(FrequencyOf_allele1_Namhae) + '\t' + str(FrequencyOf_allele2_Namhae) + '\t' +
			str(FrequencyOf_allele1_Geoje14) + '\t' + str(FrequencyOf_allele2_Geoje14) + '\t' +
			str(FrequencyOf_allele1_Pohang) + '\t' + str(FrequencyOf_allele2_Pohang) + '\t' +
			str(FrequencyOf_allele1_YellowSea) + '\t' + str(FrequencyOf_allele2_YellowSea) + '\t' +
			str(FrequencyOf_allele1_SocMuk) + '\t' + str(FrequencyOf_allele2_SocMuk))


			locus_write = str(locus_freqs).replace('[','').replace(',','\t').replace(']', '').replace("'", '').replace(' ','').replace('\\n','').replace('\\t','\t')
			output_freqs.write(locus_write + '\n')
			filtered_genotypes.write(mystring)
		else:
			bad_locus_freqs.append(locus+'\t'+
			str(FrequencyOf_allele1_Geoje15) + '\t' + str(FrequencyOf_allele2_Geoje15) + '\t' +
			str(FrequencyOf_allele1_Boryeong) + '\t' + str(FrequencyOf_allele2_Boryeong) + '\t' +
			str(FrequencyOf_allele1_Namhae) + '\t' + str(FrequencyOf_allele2_Namhae) + '\t' +
			str(FrequencyOf_allele1_Geoje14) + '\t' + str(FrequencyOf_allele2_Geoje14) + '\t' +
			str(FrequencyOf_allele1_Pohang) + '\t' + str(FrequencyOf_allele2_Pohang) + '\t' +
			str(FrequencyOf_allele1_YellowSea) + '\t' + str(FrequencyOf_allele2_YellowSea) + '\t' +
			str(FrequencyOf_allele1_SocMuk) + '\t' + str(FrequencyOf_allele2_SocMuk))

			bad_locus_write = str(bad_locus_freqs).replace('[','').replace(',','\t').replace(']', '').replace("'", '').replace(' ','').replace('\\n','').replace('\\t','\t')
			print bad_locus_write
			blacklisted_MAF.write(bad_locus_write + '\n')
			blacklisted_genotypes.write(mystring)

#close open files
genotypes_file.close()
blacklisted_genotypes.close()
blacklisted_MAF.close()
filtered_genotypes.close()
output_freqs.close()
