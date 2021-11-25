#preprocess OSM data to load into r5r for access measurement
#specifically, add LTS values based on bike lanes

import osmium

class SimplestLTSAdder(osmium.SimpleHandler):
	def __init__(self, writer, all_4):
		osmium.SimpleHandler.__init__(self)
		self.writer = writer
		self.n_modified_ways = 0
		self.all_4 = all_4
		
	def node(self, n):
		self.writer.add_node(n)
	def way(self, way):
		if 'highway' in way.tags:
			if self.all_4 == True:
				newtags = dict(way.tags)
				newtags['lts'] = '4'
				self.writer.add_way(way.replace(tags=newtags))
			else:
				if way.tags.get('highway') == 'cycleway':
					newtags = dict(way.tags)
					newtags['lts'] = '1'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway') == 'track':
					newtags = dict(way.tags)
					newtags['lts'] = '1'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway:left') == 'track':
					newtags = dict(way.tags)
					newtags['lts'] = '1'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway:right') == 'track':
					newtags = dict(way.tags)
					newtags['lts'] = '1'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway') == 'lane' and way.tags.get('highway') in ['tertiary']:
					newtags = dict(way.tags)
					newtags['lts'] = '1'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway:left') == 'lane' and way.tags.get('highway') in ['tertiary']:
					newtags = dict(way.tags)
					newtags['lts'] = '1'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway:right') == 'lane' and way.tags.get('highway') in ['tertiary']:
					newtags = dict(way.tags)
					newtags['lts'] = '1'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway') == 'lane' and way.tags.get('highway') in ['primary','secondary','residential']:
					newtags = dict(way.tags)
					newtags['lts'] = '2'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway:left') == 'lane' and way.tags.get('highway') in ['primary','secondary','residential']:
					newtags = dict(way.tags)
					newtags['lts'] = '2'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				elif way.tags.get('cycleway:right') == 'lane' and way.tags.get('highway') in ['primary','secondary','residential']:
					newtags = dict(way.tags)
					newtags['lts'] = '2'
					self.writer.add_way(way.replace(tags=newtags))
					self.n_modified_ways += 1
				else:
					newtags = dict(way.tags)
					newtags['lts'] = '4'
					self.writer.add_way(way.replace(tags=newtags))

#filters out only highways, and either assigns all LTS 4, or assigns cycletracks LTS 1 and everything else LTS 4
def add_lts_tags(osm_filename, out_filename, all_4=False):
	writer = osmium.SimpleWriter(out_filename)
	ltsadder = SimplestLTSAdder(writer, all_4)
	ltsadder.apply_file(osm_filename)
	print('added lts=1 to', ltsadder.n_modified_ways)
    
    
add_lts_tags('unformatted_data/salvador_city.pbf','salvador_area_LTS.pbf')
ghsl_to_points('unformatted_data/salvador_pop_dens.tif', 'salvador_area_pop_points.csv')