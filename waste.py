try:
	for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10],offer_id1[11]):
		#print(j)
		course_list3.append(j)
except:
	try:
		for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10]):
			#print(j)
			course_list3.append(j)
	except:
		try:
			for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9]):
				#print(j)
				course_list3.append(j)
		except:
			try:
				for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8]):
					#print(j)
					course_list3.append(j)
			except:
				try:
					for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7]):
						#print(j)
						course_list3.append(j)
				except:
					try:
						for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6]):
							#print(j)
							course_list3.append(j)
					except:
						try:
							for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5]):
								#print(j)
								course_list3.append(j)
						except:
							try:
								for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4]):
									#print(j)
									course_list3.append(j)
							except:
								try:
									for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3]):
										#print(j)
										course_list3.append(j)
								except:
									try:
										for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2]):
											#print(j)
											course_list3.append(j)
									except:
										try:
											for j in it.product(offer_id1[0],offer_id1[1]):
												#print(j)
												course_list3.append(j)
										except:
											for j in it.product(offer_id1[0]):
												#print(j)
												course_list3.append(j)
