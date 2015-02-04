# -*- coding: utf-8 -*-
from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fb_id = db.Column(db.BigInteger, unique = True)
    fb_updated_time = db.Column(db.String(45))

    name = db.Column(db.String(45))
    email = db.Column(db.String(60), unique = True)
    uuid = db.Column(db.String(50), unique = True)
    email_verified = db.Column(db.Boolean, default = '0')
    password = db.Column(db.String(100))

    def get_rate(self, place_id):
        res = self.rates.filter(Rate.place_id == place_id)
        if res.count() == 1:
            return res.one().value
        else:
            return 0




class Area(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    name = db.Column(db.String(45))

class SubArea(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    name = db.Column(db.String(45))

    parent_id = db.Column(db.Integer, db.ForeignKey('area.id',onupdate="CASCADE", ondelete="CASCADE"))
    parent = db.relationship('Area',
        backref = db.backref('subareas', cascade = 'all, delete-orphan', lazy = 'dynamic'))


class ContentType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45))

class Category1(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(45), unique = True)
    name = db.Column(db.String(45))

class Category2(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(45), unique = True)
    name = db.Column(db.String(45))
    parent_id = db.Column(db.Integer, db.ForeignKey('category1.id',onupdate="CASCADE", ondelete="CASCADE"))
    parent = db.relationship('Category1',
        backref = db.backref('subcategories', cascade = 'all, delete-orphan', lazy = 'dynamic'))

class Category3(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(45), unique = True)
    name = db.Column(db.String(45))
    parent_id = db.Column(db.Integer, db.ForeignKey('category2.id',onupdate="CASCADE", ondelete="CASCADE"))
    parent = db.relationship('Category2',
        backref = db.backref('subcategories', cascade = 'all, delete-orphan', lazy = 'dynamic'))




class Place(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)

    name = db.Column(db.Text)

    address = db.Column(db.Text)

    image_url = db.Column(db.String(2048))
    thumbnail_url = db.Column(db.String(2048))


    modified_date = db.Column(db.Date)
    read_count = db.Column(db.Integer)
    rank = db.Column(db.Float, index = True)

    tel = db.Column(db.Text)
    zip_code = db.Column(db.String(45))

    lat = db.Column(db.Numeric(20,16))
    lng = db.Column(db.Numeric(20,16))

    sub_area_id = db.Column(db.Integer, db.ForeignKey('sub_area.id', onupdate="CASCADE", ondelete="SET NULL"))
    sub_area = db.relationship('SubArea', 
        backref = db.backref('places', cascade = 'all, delete-orphan', lazy = 'dynamic'))

    content_type_id = db.Column(db.Integer, db.ForeignKey('content_type.id', onupdate="CASCADE", ondelete="SET NULL"))
    content_type = db.relationship('ContentType', 
        backref = db.backref('places', cascade = 'all, delete-orphan', lazy = 'dynamic'))

    category_id = db.Column(db.Integer, db.ForeignKey('category3.id', onupdate="CASCADE", ondelete="SET NULL"))
    category = db.relationship('Category3',
        backref = db.backref('places', cascade = 'all, delete-orphan', lazy = 'dynamic'))

    rate_count = db.Column(db.Integer, default = '0')
    rate_sum = db.Column(db.Integer, default = '0')

    best_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', onupdate="CASCADE", ondelete="SET NULL", use_alter=True, name='fk_best_comment_id'), nullable = True)
    best_comment = db.relationship('Comment', foreign_keys='Place.best_comment_id')

    best_place_image_id = db.Column(db.Integer, db.ForeignKey('place_image.id', onupdate = "CASCADE", ondelete="SET NULL", use_alter = True, name='fk_best_place_image_id'), nullable = True)

    best_place_image = db.relationship('PlaceImage', foreign_keys = 'Place.best_place_image_id')


    @staticmethod
    def get_card_data_list(offset, limit, user_id = None, rated = False, keyword = None):

        query = """
        SELECT 
            p.id, p.name, p.thumbnail_url, p.rate_count, p.rate_sum, a.name area, c.name content_type, p.best_comment_id, bc.body best_comment_body, bcu.name best_comment_username """+(', r.value rated_value' if user_id else '')+"""
        FROM place p
        LEFT JOIN sub_area sa
        ON p.sub_area_id = sa.id
        LEFT JOIN area a
        ON sa.parent_id = a.id
        LEFT JOIN content_type c
        ON p.content_type_id = c.id
        LEFT JOIN comment bc
        ON p.best_comment_id = bc.id
        LEFT JOIN user bcu
        ON bc.user_id = bcu.id
        """
        if user_id:
            query += """
        LEFT JOIN rate r
        ON p.id = r.place_id
        AND r.user_id = '"""+str(user_id)+"""'

        """

        if user_id:
            query += """
            WHERE r.id is """+('not' if rated else '')+""" null
            """

        if keyword:
            if user_id:
                query += """ AND p.name LIKE :keyword """
            else:
                query += """ WHERE p.name LIKE :keyword """
        query += """
        ORDER BY rank DESC
        LIMIT """+str(offset)+""","""+str(limit)+"""
        
        """
        if keyword:
            res = db.session.execute(query, {'keyword':'%'+keyword+'%'})    
        else:
            res = db.session.execute(query)

        data = []
        for row in res:
            row = dict(zip(row.keys(), row))
            d = {
                'id':row['id'],
                'name':row['name'],
                'thumbnailUrl':row['thumbnail_url'],
                'rateCount':row['rate_count'],
                'rateSum':row['rate_sum'],
                'area':row['area'],
                'contentType':row['content_type']
            }

            if user_id and row['rated_value']:
                d['rated'] = True
                d['ratedValue'] = row['rated_value']

            if row['best_comment_id']:
                d['bestComment'] = {
                    'id':row['best_comment_id'],
                    'username':row['best_comment_username'],
                    'body':row['best_comment_body']
                }
            data.append(d)

        return data



    def get_card_data(self, user_id = None):
        data = {
            'id': self.id,
            'name': self.name,
            'thumbnailUrl': self.thumbnail_url,
            'rateCount': self.rate_count,
            'rateSum': self.rate_sum,
            'area': self.sub_area.parent.name,
            'contentType': self.content_type.name
        }

        if user_id:
            rate = self.get_rate_by_user_id(user_id)
            if rate:
                data['rated'] = True
                data['ratedValue'] = rate.value

        best_comment = self.get_best_comment()
        if best_comment:
            data['bestComment'] = {
                'id': best_comment.id,
                'username': best_comment.user.name,
                'body': best_comment.body
            }

        return data


    def add_comment(self, user_id, body):
        comment = Comment(
            place_id = self.id,
            user_id = user_id,
            body = body
            )

        db.session.add(comment)
        db.session.commit()

        if self.best_comment_id:
            if self.best_comment.like_count == 0:
                self.best_comment_id = comment.id
        else:
            self.best_comment_id = comment.id


        db.session.commit()



    def get_best_comment(self):
        return self.best_comment

    def get_top_comments(self):
        return self.comments.filter(Comment.id != self.best_comment_id).order_by(Comment.like_count.desc(), Comment.writed_time.desc()).limit(3)

    def load_comments(self, offset):
        return self.comments.filter(Comment.id != self.best_comment_id).order_by(Comment.like_count.desc(), Comment.writed_time.desc()).offset(offset).limit(5)


    def add_rate(self, user_id, rate_value):
        rate = Rate(
            user_id = user_id,
            place_id = self.id,
            value = rate_value)

        self.rate_count += 1
        self.rate_sum += rate_value


        db.session.add(rate)
        db.session.commit()

    def get_rate_by_user_id(self, user_id):
        try: 
            return self.rates.filter(Rate.user_id == user_id).one()
        except:
            return None

    def cancel_rate(self, user_id):
        rate = self.rates.filter(Rate.user_id == user_id, Rate.place_id == self.id).one()

        self.rate_count -= 1
        self.rate_sum -= rate.value

        db.session.delete(rate)
        db.session.commit()

    def get_rate_value(self):
        if self.rate_count:
            return '%.1f'%(float(self.rate_sum)/self.rate_count/2)
        else:
            return None

    def get_rate_html(self, user_id = None, with_rate_value = True):
        if not user_id:
            rate_value = self.get_rate_value()
        else:
            try:
                rate_value = '%.1f'%(float(self.get_rate_by_user_id(user_id).value)/2)
            except: 
                rate_value = None

        if not rate_value:
            if user_id:
                average_rate_string = ''
            else:
                average_rate_string = u'<span class="small">아직 평가가 없어요</span>'
        else:
            average_rate_string = ''
            for i in range(int(float(rate_value))):
                average_rate_string += '<span class="fa fa-star"></span>'

            if float(rate_value) - int(float(rate_value)) > 0.2:
                average_rate_string += '<span class="fa fa-star-half"></span>'

            if with_rate_value:
                average_rate_string += ' ' + rate_value
        return average_rate_string

    def get_rate_area_html(self, user_id = None, with_wrapper = True, ):

        try:
            rate = self.get_rate_by_user_id(user_id)
        except:
            rate = None

        html = ''

        if with_wrapper:
            html += '<div class="panel-footer text-center rate-area'+(' rated' if (rate and rate.value) else '')+'">'
        if rate and rate.value:
            for i in range(int(rate.value/2)):
                html += '<span class="fa fa-star active" data-value="'+str(i*2+2)+'"></span>'
            if rate.value%2:
                html += '<span class="fa fa-star-half-o active" data-value="'+str(rate.value+1)+'"></span>'
            for i in range( int((10-rate.value)/2) ):
                html += '<span class="fa fa-star-o" data-value="'+str( (int((rate.value+3)/2)+i)*2 )+'"></span>'
        else:
            html += '<span class="fa fa-star-o" data-value="2"></span><span class="fa fa-star-o" data-value="4"></span><span class="fa fa-star-o" data-value="6"></span><span class="fa fa-star-o" data-value="8"></span><span class="fa fa-star-o" data-value="10"></span>'

        if with_wrapper:
            html += '</div>'

        return html

    # def add_image(self, user_id, image_url):
    #     picture_image = PictureImage(
    #         user_id = user_id,
    #         place_id = self.id
    #         )


    def add_image(self, user_id, image_url, thumbnail_url):
        place_image = PlaceImage(
            place_id = self.id,
            user_id = user_id,
            image_url = image_url,
            thumbnail_url = thumbnail_url
            )

        db.session.add(place_image)
        db.session.commit()

        if not self.best_place_image_id:
            self.best_place_image_id = place_image.id
            self.image_url = place_image.image_url
            self.thumbnail_url = place_image.thumbnail_url

            db.session.commit()








class Rate(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rated_time = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())
    value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship('User',
        backref = db.backref('rates', cascade = 'all, delete-orphan', lazy = 'dynamic'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id', onupdate="CASCADE", ondelete="CASCADE"))
    place = db.relationship('Place',
        backref = db.backref('rates', cascade = 'all, delete-orphan', lazy = 'dynamic'))
    __table_args__ = (db.UniqueConstraint('user_id', 'place_id', name='unq_rate_uid_pid'),
                     )



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    like_count = db.Column(db.Integer, index = True, default = '0')
    writed_time = db.Column(db.DateTime, default=db.func.now(), index = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship('User',
        backref = db.backref('comments', cascade = 'all, delete-orphan', lazy = 'dynamic'))


    place_id = db.Column(db.Integer, db.ForeignKey('place.id', onupdate="CASCADE", ondelete="CASCADE"))
    place = db.relationship('Place',
        foreign_keys='Comment.place_id',
        backref = db.backref('comments', cascade = 'all, delete-orphan', lazy = 'dynamic'))

    def is_liked_by(self, user_id):
        return self.likes.filter(CommentLike.user_id == user_id).count() == 1

    def like(self, user_id):
        comment_like = CommentLike(
            user_id = user_id,
            comment_id = self.id)
        self.like_count += 1

        if self.place.best_comment.like_count < self.like_count:
            self.place.best_comment_id = self.id

        db.session.add(comment_like)
        db.session.commit()

        


    def like_cancel(self, user_id):
        comment_like = CommentLike.query.filter(
            CommentLike.user_id == user_id,
            CommentLike.comment_id == self.id
            ).one()

        self.like_count -= 1
        db.session.delete(comment_like)
        db.session.commit()





class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship('User')

    liked_time = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', onupdate="CASCADE", ondelete="CASCADE"))
    comment = db.relationship('Comment',
        backref = db.backref('likes', cascade = 'all, delete-orphan', lazy = 'dynamic'))
    liked_time = db.Column(db.DateTime, default = db.func.now(), onupdate=db.func.now())


    __table_args__ = (db.UniqueConstraint('user_id', 'comment_id', name='unq_comment_like_uid_cid'),
                     )
    
class PlaceImage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    flickr_id = db.Column(db.BigInteger, unique = True, nullable = True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id', onupdate="CASCADE", ondelete="CASCADE"))
    place = db.relationship('Place',
        foreign_keys = 'PlaceImage.place_id',
        backref = db.backref('images', cascade ='all, delete-orphan', lazy = 'dynamic'))
    thumbnail_url = db.Column(db.String(2048))
    image_url = db.Column(db.String(2048))
    like_count = db.Column(db.Integer, default = '0', index = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="SET NULL"), nullable = True)
    user = db.relationship('User', backref = db.backref('upload_images', cascade = 'all, delete-orphan', lazy = 'dynamic'))

    def like(self, user_id):
        image_like = ImageLike(
            place_image_id = self.id,
            user_id = user_id
            )

        self.like_count += 1

        db.session.add(image_like)

        current_best_image = self.place.best_place_image

        if current_best_image and self.like_count > current_best_image.like_count:
            self.place.best_place_image_id = self.id
            self.place.image_url = self.image_url
            self.place.thumbnail_url = self.thumbnail_url

        db.session.commit()

    def is_liked_by(self, user_id):
        return self.liked_users.filter(ImageLike.user_id == user_id).count() > 0




class ImageLike(db.Model):
    id = db.Column(db.Integer, primary_key = True)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
        onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship('User', 
        backref = db.backref('liked_images', cascade ='all, delete-orphan', lazy = 'dynamic'))
    liked_time = db.Column(db.DateTime, default = db.func.now())

    place_image_id = db.Column(db.Integer, db.ForeignKey('place_image.id', onupdate="CASCADE", ondelete="CASCADE"))
    place_image = db.relationship('PlaceImage', 
        backref = db.backref('liked_users',cascade='all, delete-orphan', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint('user_id', 'place_image_id', name='unq_image_like_uid_pid'),
                     )











