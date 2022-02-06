import csv


# Should this actually be a class?
class Process:

    def __init__(self, signer, company, image_path, vt_permalink, vt_detection=None):
        self.signer = signer
        self.company = company
        self.image_path = image_path
        self.vt_detection = vt_detection
        self.vt_permalink = vt_permalink

    def get_signer(self):
        return self.signer

    def get_company(self):
        return self.company

    def get_image_path(self):
        return self.image_path

    def get_vt_detection(self):
        return self.vt_detection

    def get_vt_permalink(self):
        return self.vt_permalink

    # Display vt score and link
    def vt_str(self):
        return f'VT Score: {self.vt_detection}, {self.vt_permalink}'

    # Display full object...Looks ugly. need to fix
    def __str__(self):
        return f'{self.signer},{self.company},{self.image_path},{self.vt_detection},{self.vt_permalink}'

    def find_vt_score(self):
        """Finds the first number in vt detection field and returns as integer."""
        vt_str = str(self.vt_detection).split('|')
        score = vt_str[0]
        if score.isdigit():
            return int(score)
        return None
