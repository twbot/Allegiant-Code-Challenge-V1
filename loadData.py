#!/usr/bin/env python3
import csv
import os
import mysql.connector as connector
from mysql.connector import errorcode
import argparse

maps = []
data = []
dicts = []

#Database to create if !exist
Database_Name = 'customers'
# Predefined table structure
# Ideally this would be created via a user interface and then exported into
# this script but this will do for now 
tables = {}
tables['customers'] = (
"CREATE TABLE `customers` ("
"  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,"
"  `created_at` datetime NOT NULL,"
"  `first_name` varchar(30) DEFAULT NULL,"
"  `last_name` varchar(50) DEFAULT NULL,"
"  `email` varchar(255) NOT NULL DEFAULT '',"
"  `latitude` float(10,6) DEFAULT NULL,"
"  `longitude` float(10,6) DEFAULT NULL,"
"  `ip` varchar(15) DEFAULT NULL,"
"  PRIMARY KEY (`id`),"
"  UNIQUE KEY `UNIQUE_EMAIL` (`email`)"
") ENGINE=InnoDB")

def determine_file_types(files):
	for file in files:
		if file.__contains__('map'):
			maps.append(file)
			dicts.append({})
		else:
			data.append(file)
	data.sort()
	maps.sort()

def determine_csv_layout(directory):
	for map_ in maps:
		with open(os.path.join(directory, map_),newline='') as csv_file:
			csv_reader = csv.reader(csv_file)
			index = maps.index(map_)
			rows = []
			for row in csv_reader:
				rows.append(row)
			for i in range(len(rows[0])):
				dicts[index][rows[0][i]] = rows[1][i]

def create_table(cursor):
	global tables
	# Create table in customers database
	for table_name in tables:
		table_description = tables[table_name]
		try:
			print("Creating table {}: ...".format(table_name))
			cursor.execute(table_description)
		except connector.Error as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print("Table {} already exists: deleting...".format(table_name))
				cursor.execute('DROP TABLE `customers`;')
				create_table(cursor)
			else:
				print(err.msg)
		else:
			print("OK")

def create_database(cursor):
	try:
		cursor.execute( \
		"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(Database_Name))
	except connector.Error as err:
		print("Failed creating database: {}".format(err))
		pass
	try:
		cursor.execute("USE {}".format(Database_Name))
		print("Using Database: {}".format(Database_Name))
	except connector.Error as err:
		print("Database {} does not exist.".format(Database_Name))
		if err.errno == errorcode.ER_BAD_DB_ERROR:
			create_database(cursor)
			print("Database {} created successfully.".format(Database_Name))
			cnx.database = Database_Name
		else:
			print(err)
			exit(1)

def insert_data(directory, cursor):
	# SQL Insert Definition
	add_customer = ("INSERT INTO customers "
               "(created_at, first_name, last_name, email, latitude, longitude, ip) "
               "VALUES (%s, %s, %s, %s, %s, %s ,%s)")

	for data_ in data:
		index = data.index(data_)
		with open(os.path.join(directory, data_),newline='') as csv_file:
			csv_reader = csv.reader(csv_file)
			headers = next(csv_reader, None)
			column = {}
			for header in headers:
				column[header] = []
			for row in csv_reader:
				for header, v in zip(headers, row):
					if(v == ''):
						column[header].append('')
					else:
						column[header].append(v)
			customers = [
				column[dicts[index]['created_at']], \
				[x if x != '' else None for x in column[dicts[index]['first_name']]], \
				[x if x != '' else None for x in column[dicts[index]['last_name']]], \
				column[dicts[index]['email']], \
				[round(float(x),6) if x != '' else None for x in column[dicts[index]['latitude']]], \
				[round(float(x),6) if x != '' else None for x in column[dicts[index]['longitude']]], \
				column[dicts[index]['ip']]]

			num_customers = len(customers[0])
			for i in range(num_customers):
				customer = ( \
					customers[0][i], \
					customers[1][i], \
					customers[2][i], \
					customers[3][i], \
					customers[4][i], \
					customers[5][i], \
					customers[6][i] \
					)
				try:
					cursor.execute(add_customer, customer)
				except connector.Error as err:
					print(err)
					print(customers[4][i])
					exit(1)

def main(directory, password):
	# Determine mapping from files
	files = os.listdir(directory)
	determine_file_types(files)
	determine_csv_layout(directory)

	# Connect to mysql and create database + table
	try:
		database = 	connector.connect( \
			user='root', \
			password=password, \
			allow_local_infile=False)
	except connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Wrong password for user: root")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)

	cursor = database.cursor()
	create_database(cursor)
	create_table(cursor)

	#Insert data into customers table
	insert_data(directory, cursor)
	print("Data successfully added into table")
	database.commit()
	print("Closing connection...")
	cursor.close()
	database.close()
	print("Closed")

	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file_directory', help='Directory where files are located')
	parser.add_argument('--password', help='Password for MySQL root user', required=False)
	args = parser.parse_args()
	main(args.file_directory, args.password)
