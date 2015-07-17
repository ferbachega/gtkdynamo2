
#filein  = raw_input("filein: ")
#fileout = raw_input("fileout: ")


def amber12_to_amber11_topology_converter (filein, fileout):
	filein = open(filein, 'r')
	text   = []
	print_line = True

	for line in filein:
		line2 = line.split()
		try:
			if line2[0] == '%FLAG':
				if   line2[1] == 'ATOMIC_NUMBER':
					print 'excluding flag:', line
					print_line = False

				elif   line2[1] == 'SCEE_SCALE_FACTOR':
					print 'excluding flag:', line
					print_line = False

				elif   line2[1] == "SCNB_SCALE_FACTOR":
					print 'excluding flag:', line
					print_line = False			

				elif   line2[1] == 'IPOL':
					print 'excluding flag:', line
					print_line = False
		
				else:
					print_line = True	
					#print print_line
		except:
			a= None
		if print_line == True:
			text.append(line)

	fileout = open(fileout, 'w')
	fileout.writelines(text)
	fileout.close()



#def main():
#    amber12_to_amber11_topology_converter (filein, fileout)
#    return 0
#
#if __name__ == '__main__':
#	main()
#
