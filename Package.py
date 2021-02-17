# Milan Macura #000989289

class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, weight, notes=None):
        # The id for each package
        self.package_id = package_id
        self.address = address
        # Destination
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        # How much the package weighs
        self.weight = weight
        self.notes = notes
        # Delivery status
        self.delivered = 'HUB'
        self.delivery_time = None

    # Set the delivery status to delivered
    def deliver(self, delivery_time):
        self.delivered = 'Delivered'
        self.delivery_time = delivery_time
