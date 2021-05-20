# (C) Copyright 2019 Hewlett Packard Enterprise Development LP.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# __author__ = "@netwookie"
# __credits__ = ["Rick Kauffman"]
# __license__ = "Apache2.0"
# __version__ = "1.0.0"
# __maintainer__ = "Rick Kauffman"
# __email__ = "rick.a.kauffman@hpe.com"

from mongoengine import signals

from application import db

class Volumes(db.Document):
    name = db.StringField(db_field="n", required=True)
    dedupe = db.StringField(db_field="d", required=True)
    block_size = db.StringField(db_field="b", required=True)
    online = db.StringField(db_field="o", required=True)
    thin = db.StringField(db_field="t", required=True)
    encrypt = db.StringField(db_field="e", required=True)
