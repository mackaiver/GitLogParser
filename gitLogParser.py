#!/usr/bin/env python

import sys
import re

# array to store dict of commit data
commits = []
files_changed_pattern = re.compile(' (\\d+) files* changed')
insertion_pattern = re.compile('\\s(\\d+) insertions*')
deletion_pattern = re.compile('\\s(\\d+) deletions*')

def parseCommit(commitLines):
	# dict to store commit data
	commit = {}

	# iterate lines and save
	for commit_line in commitLines:
		# print(commit_line)
		if commit_line == '' or commit_line == '\n':
			# ignore empty lines
			pass
		elif bool(re.match('commit', commit_line, re.IGNORECASE)):
			# commit xxxx
			# if len(commit) != 0:		## new commit, so re-initialize
			commit = {'hash' : re.match('commit (.*)', commit_line, re.IGNORECASE).group(1) }
			commit['files_changed'] = 0
			commit['insertions'] = 0
			commit['deletions'] = 0
			commits.append(commit)

		elif bool(re.match('merge:', commit_line, re.IGNORECASE)):
			# Merge: xxxx xxxx
			pass
		elif bool(re.match('author:', commit_line, re.IGNORECASE)):
			# Author: xxxx <xxxx@xxxx.com>
			m = re.compile('Author: (.*) <(.*)>').match(commit_line)
			commit['author'] = m.group(1)
			commit['email'] = m.group(2)
		elif bool(re.match('date:', commit_line, re.IGNORECASE)):
			m = re.match('Date:\s+(.+)', commit_line)
			if m:
				commit['date'] = m.group(1)
			pass
		elif bool(re.match('    ', commit_line, re.IGNORECASE)):
			# (4 empty spaces)
			if commit.get('message') is None:
				commit['message'] = commit_line.strip().replace(';', ',')
		else:
			if files_changed_pattern.search(commit_line):
				m = files_changed_pattern.search(commit_line)
				if m:
					commit['files_changed'] = m.group(1)

			if insertion_pattern.search(commit_line):
				m = insertion_pattern.search(commit_line)
				if m:
					commit['insertions'] = m.group(1)

			if deletion_pattern.search(commit_line):
				m = deletion_pattern.search(commit_line)
				if m:
					commit['deletions'] = m.group(1)


if __name__ == '__main__':
	parseCommit(sys.stdin.readlines())
	print('author;email;date;hash;message;files_changed;insertions;deletions')
	for commit in commits:
		print('{};{};{};{};{};{};{};{}'
					.format(commit['author'],
							commit['email'],
							commit['date'],
							commit['hash'],
							commit['message'],
							commit['files_changed'],
							commit['insertions'],
							commit['deletions']))
