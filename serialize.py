def serialize(sender, clock, event_id):
	return str.encode((sender)+'\t'+str(clock)+'\t'+str(event_id)+'\n')

def deserialize(msg):
	return msg.split('\t')

