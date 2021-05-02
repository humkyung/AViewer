# coding: utf-8
"""This is SDNFLinearMember module"""

import enum
from SDNFElement import SDNFElement


class SDNFLinearMember(SDNFElement):
    """This is SDNFLinearMember class"""

    class ElmType(enum.Enum):
        NONE = 0
        BEAM = 1
        COLUMN = 2
        HBRACE = 3
        VBRACE = 4

    def __init__(self):
        self._member_type = SDNFLinearMember.ElmType.NONE
        self._record1 = SDNFLinearMember.Record1()
        self._record2 = SDNFLinearMember.Record2()
        self._record3 = SDNFLinearMember.Record3()
        self._record4 = SDNFLinearMember.Record4()
        self._record5 = SDNFLinearMember.Record5()
        self._record6 = SDNFLinearMember.Record6()
        self._record7 = SDNFLinearMember.Record7()
        self._record8 = SDNFLinearMember.Record8()
        self._record9 = SDNFLinearMember.Record9()
        self._record10 = SDNFLinearMember.Record10()

    def parse(self, file, start):
        """parse linear member"""
        from SDNFFile import SDNFFile

        try:
            self._record1.parse(start)

            line = file.readline().strip()
            self._record2.parse(line)

            line = file.readline().strip()
            self._record3.parse(line)

            line = file.readline().strip()
            self._record4.parse(line)

            line = file.readline().strip()
            self._record5.parse(line)

            line = file.readline().strip()
            self._record6.parse(line)

            if SDNFFile.VER == SDNFFile.Ver.VER_3:
                line = file.readline().strip()
                self._record7.parse(line)

                line = file.readline().strip()
                self._record8.parse(line)

                line = file.readline().strip()
                self._record9.parse(line)

                line = file.readline().strip()
                self._record10.parse(line)
        except Exception as ex:
            raise ex

    @property
    def member_id(self):
        return self._record1.member_id

    @property
    def cardinal_point(self):
        return self._record1.cardinal_point

    @property
    def member_type(self):
        return self._member_type

    @property
    def member_type_string(self):
        res = 'NONE'

        if self._member_type == SDNFLinearMember.ElmType.BEAM:
            res = 'BEAM'
        elif self._member_type == SDNFLinearMember.ElmType.COLUMN:
            res = 'COLUMN'
        elif self._member_type == SDNFLinearMember.ElmType.HBRACE:
            res = 'HBRACE'
        elif self._member_type == SDNFLinearMember.ElmType.VBRACE:
            res = 'VBRACE'

        return res

    @property
    def section(self):
        return self._record2.section_size

    @property
    def grade(self):
        return self._record2.grade

    @property
    def rotation(self):
        return self._record2.rotation

    @property
    def ori_vector(self):
        return self._record3.ori_vector

    @property
    def w(self):
        import math

        res = SDNFLinearMember.cross_product(self.direction, self.ori_vector)
        factor = 1. / math.sqrt(res[0] * res[0] + res[1] * res[1] + res[2] * res[2])
        res[0] *= factor
        res[1] *= factor
        res[2] *= factor

        return res

    @property
    def v(self):
        import math

        res = SDNFLinearMember.cross_product(self.w, self.direction)
        factor = 1. / math.sqrt(res[0] * res[0] + res[1] * res[1] + res[2] * res[2])
        res[0] *= factor
        res[1] *= factor
        res[2] *= factor

        return res

    @property
    def direction(self):
        import math

        _end, _start = self.end(), self.start()
        res = [_end[0] - _start[0], _end[1] - _start[1], _end[2] - _start[2]]
        factor = 1. / math.sqrt(res[0] * res[0] + res[1] * res[1] + res[2] * res[2])
        res[0] *= factor
        res[1] *= factor
        res[2] *= factor

        return res

    @staticmethod
    def cross_product(u, v):
        """return cross product of given two vectors"""
        res = [u[1] * v[2] - v[1] * u[2], v[0] * u[2] - u[0] * v[2], u[0] * v[1] - v[0] * u[1]]
        return res

    def start(self, unit=SDNFElement.UNIT.NONE):
        if unit == SDNFElement.UNIT.NONE or unit == self.unit:
            return self._record3.start

        if SDNFElement.UNIT.METER == self.unit and SDNFElement.UNIT.MILLIMETER == unit:
            return self._record3.start * 1000
        elif SDNFElement.UNIT.METER == self.unit and SDNFElement.UNIT.CENTIMETER == unit:
            return self._record3.start * 100
        elif SDNFElement.UNIT.CENTIMETER == self.unit and SDNFElement.UNIT.MILLIMETER == unit:
            return self._record3.start * 10
        elif SDNFElement.UNIT.CENTIMETER == self.unit and SDNFElement.UNIT.METER == unit:
            return self._record3.start * 0.01
        elif SDNFElement.UNIT.MILLIMETER == self.unit and SDNFElement.UNIT.METER == unit:
            return self._record3.start * 0.001
        elif SDNFElement.UNIT.MILLIMETER == self.unit and SDNFElement.UNIT.ENTIMETER == unit:
            return self._record3.start * 0.1

        return self._record3.start

    def end(self, unit=SDNFElement.UNIT.NONE):
        if unit == SDNFElement.UNIT.NONE or unit == self.unit:
            return self._record3.end

        if SDNFElement.UNIT.METER == self.unit and SDNFElement.UNIT.MILLIMETER == unit:
            return self._record3.end * 1000
        elif SDNFElement.UNIT.METER == self.unit and SDNFElement.UNIT.CENTIMETER == unit:
            return self._record3.end * 100
        elif SDNFElement.UNIT.CENTIMETER == self.unit and SDNFElement.UNIT.MILLIMETER == unit:
            return self._record3.end * 10
        elif SDNFElement.UNIT.CENTIMETER == self.unit and SDNFElement.UNIT.METER == unit:
            return self._record3.end * 0.01
        elif SDNFElement.UNIT.MILLIMETER == self.unit and SDNFElement.UNIT.METER == unit:
            return self._record3.end * 0.001
        elif SDNFElement.UNIT.MILLIMETER == self.unit and SDNFElement.UNIT.ENTIMETER == unit:
            return self._record3.end * 0.1

        return self._record3.end

    class Record1:
        """This is Record1 class"""

        def __init__(self):
            self.member_id = None
            self.cardinal_point = None
            self.status = None  # FrameWorks Plus always sets this to 0
            self._class = None  # Member class from 0 to 9. 0=Primary, 1=Secondary,2=Tertiary, 3=User1, 4=User2, 5, 6, 7, 8, 9
            self.type = None
            self.piece_mark = None  # FrameWorks Plus member name
            self.rev_no = None  # Always set to 1 by FrameWorks Plus

        def parse(self, line):
            """parse Record1"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 7 == len(tokens):
                self.member_id = tokens[0]
                self.cardinal_point = int(tokens[1])
                self.status = int(tokens[2])
                self._class = int(tokens[3])
                self.type = tokens[4]
                self.piece_mark = tokens[5]
                self.rev_no = int(tokens[6])

    class Record2:
        def __init__(self):
            self.section_size = None  # Section size assigned to the member
            self.grade = None  # Material grade name assigned to the member
            self.rotation = None  # Rotation of section: 0, 90, 180, 270
            self.mirror_x_axis = None  # 0 is no reflect
            self.mirror_y_axis = None  # 1 is reflect about Y axis; 0 is no reflect

        def parse(self, line):
            """parse Record2"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 5 == len(tokens):
                self.section_size = tokens[0]
                self.grade = tokens[1]
                self.rotation = float(tokens[2])
                self.mirror_x_axis = int(tokens[3])
                self.mirror_y_axis = tokens[4]

    class Record3:
        def __init__(self):
            self.ori_vector = None  # Orientation Vector
            self.start = None  # Start Coordinates
            self.end = None  # End Coordinates
            self.end_cutbacks = None
            self.start_cutbacks = None

        def parse(self, line):
            """parse Record3"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 11 == len(tokens):
                self.ori_vector = [float(tokens[0]), float(tokens[1]), float(tokens[2])]
                self.start = [float(tokens[3]), float(tokens[4]), float(tokens[5])]
                self.end = [float(tokens[6]), float(tokens[7]), float(tokens[8])]
                self.end_cutbacks = float(tokens[9])
                self.start_cutbacks = float(tokens[10])

    class Record4:
        def __init__(self):
            self.x_cross_section_offset = None  # Offset of the cross-section relative to the x-axis of the section
            self.y_cross_section_offset = None  # Offset of the cross-section relative to the y-axis of the section

        def parse(self, line):
            """parse Record4"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 2 == len(tokens):
                self.x_cross_section_offset = float(tokens[0])
                self.y_cross_section_offset = float(tokens[1])

    class Record5:
        def __init__(self):
            self.start_offset = None  # Rigid end offset at the start of the member
            self.end_offset = None  # Rigid end offset at the end of the member

        def parse(self, line):
            """parse Record5"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 6 == len(tokens):
                self.start_offset = [float(tokens[0]), float(tokens[1]), float(tokens[2])]
                self.end_offset = [float(tokens[3]), float(tokens[4]), float(tokens[5])]

    class Record6:
        def __init__(self):
            # 0 - No release for that Degree of Freedom, 1 - Release for that Degree of Freedom
            self.end_1_x, self.end_1_y, self.end_1_z = None, None, None
            # 0 - No release for that Degree of Freedom, 1 - Release for that Degree of Freedom
            self.end_1_rx, self.end_1_ry, self.end_1_rz = None, None, None
            # 0 - No release for that Degree of Freedom, 1 - Release for that Degree of Freedom
            self.end_2_x, self.end_2_y, self.end_2_z = None, None, None
            # 0 - No release for that Degree of Freedom, 1 - Release for that Degree of Freedom
            self.end_2_rx, self.end_2_ry, self.end_2_rz = None, None, None

        def parse(self, line):
            """parse Record6"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 12 == len(tokens):
                self.end_1_x, self.end_1_y, self.end_1_z = int(tokens[0]), int(tokens[1]), int(tokens[2])
                self.end_1_rx, self.end_1_ry, self.end_1_rz = int(tokens[3]), int(tokens[4]), int(tokens[5])
                self.end_2_x, self.end_2_y, self.end_2_z = int(tokens[6]), int(tokens[7]), int(tokens[8])
                self.end_2_rx, self.end_2_ry, self.end_2_rz = int(tokens[9]), int(tokens[10]), int(tokens[11])

    class Record7:
        def __init__(self):
            self.fabricator_id = None  # FrameWorks initialize this field to 0
            self.pre_buy_mark = None  # FrameWorks initialize this field to empty string
            self.sub_type = None  # Code listed value from the FrameWorks Plus attribute.dat file
            self.creation_date = None  # Date member was created in authoring package
            self.creation_time = None  # Time member was created in authoring package
            self.modification_date = None  # Date member was modified in authoring package
            self.modification_time = None  # Time member was modified in authoring package
            self.updated = None  # Indicates whether fabricator/detailer has updated the member.
            # 1 = Member was updated, 0 = Member has not been updated
            self.approval_status = None  # Not used by FrameWorks Plus

        def parse(self, line):
            """parse Record7"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 9 == len(tokens):
                self.fabricator_id = int(tokens[0])
                self.pre_buy_mark = tokens[1]
                self.sub_type = int(tokens[2])
                self.creation_date = tokens[3]
                self.creation_time = tokens[4]
                self.modification_date = tokens[5]
                self.modification_time = tokens[6]
                self.updated = int(tokens[7])
                self.approval_status = int(tokens[8])

    class Record8:
        def __init__(self):
            self.connection_at_end1 = None  # Type of end combination at member end 1. Code listed value from the FormWorks Plus attribute.dat file. 0 if not defined
            self.end1_connecting_member1 = None  # Member ID of supporing member at end 1. 0 if no member
            self.end1_connecting_member2 = None  # Member ID of supporing member at end 1. 0 if no member
            self.end1_connecting_member3 = None  # Member ID of supporing member at end 1. 0 if no member
            self.connection_at_end2 = None  # Type of end combination at member end 2. Code listed value from the FormWorks Plus attribute.dat file. 0 if not defined
            self.end2_connecting_member1 = None  # Member ID of supporing member at end 2. 0 if no member
            self.end2_connecting_member2 = None  # Member ID of supporing member at end 2. 0 if no member
            self.end2_connecting_member3 = None  # Member ID of supporing member at end 2. 0 if no member
            self.connection_configuration = None  # Not used by FrameWorks Plus
            self.assembly1 = None  # Associates other members to this member. Code listed value from the FrameWorks Plus attributes.dat file. 0 if no Assembly
            self.assembly2 = None  # Associates other members to this member. Code listed value from the FrameWorks Plus attributes.dat file. 0 if no Assembly
            self.assembly3 = None  # Associates other members to this member. Code listed value from the FrameWorks Plus attributes.dat file. 0 if no Assembly

        def parse(self, line):
            """parse Record8"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 12 == len(tokens):
                self.connection_at_end1 = int(tokens[0])
                self.end1_connecting_member1 = int(tokens[1])
                self.end1_connecting_member2 = int(tokens[2])
                self.end1_connecting_member3 = int(tokens[3])
                self.connection_at_end2 = int(tokens[4])
                self.end2_connecting_member1 = int(tokens[5])
                self.end2_connecting_member1 = int(tokens[6])
                self.end2_connecting_member1 = int(tokens[7])
                self.connection_configuration = int(tokens[8])
                self.assembly1 = int(tokens[9])
                self.assembly2 = int(tokens[10])
                self.assembly3 = int(tokens[11])

    class Record9:
        def __init__(self):
            self.material = None  # 0 = Steel, 1 = Concrete, 2 = Aluminum, 3 = Plastic, 4 = Timbler, 5 = Other
            self.coating = None  # Code listed value from the FrameWorks Plus attributes.dat file
            self.fire_proofing_thickness = None  # Thickness of the fireproofing. Value is always inches or milimierters based on member units.
            self.fire_proofing_description = None  # 0 = None, 1 = Contour, fully encased, 2 = Contour,top flange exposed, 3 = Block, fully encased, 4 = Block, top flange exposed
            self.fire_proofing_type = None  # 0 = Shop Applied, 1 = Field Applied
            self.fire_proofing_start = None  # Distance from the start of the member to point where fireproofing begins.
            self.fire_proofing_end = None  # Distance from the start of the member to point where fireproofing ends.

        def parse(self, line):
            """parse Record9"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 7 == len(tokens):
                self.material = int(tokens[0])
                self.coating = int(tokens[1])
                self.fire_proofing_thickness = float(tokens[2])
                self.fire_proofing_description = int(tokens[3])
                self.fire_proofing_type = int(tokens[4])
                self.fire_proofing_start = float(tokens[5])
                self.fire_proofing_end = float(tokens[6])

    class Record10:
        def __init__(self):
            self.fabricator_note = None  # Any special note from fabricator. Code listed value from the FrameWorks Plus attributes.dat file
            self.user_attribute1 = None  # Code listed value from the FrameWorks Plus attributes.dat file
            self.user_attribute2 = None  # Code listed value from the FrameWorks Plus attributes.dat file
            self.user_attribute3 = None  # Code listed value from the FrameWorks Plus attributes.dat file
            self.user_attribute4 = None  # Code listed value from the FrameWorks Plus attributes.dat file
            self.user_attribute5 = None  # Code listed value from the FrameWorks Plus attributes.dat file

        def parse(self, line):
            """parse Record10"""

            tokens = line.split()
            tokens = [token for token in tokens if token]
            if 6 == len(tokens):
                self.fabricator_note = int(tokens[0])
                self.user_attribute1 = int(tokens[1])
                self.user_attribute2 = int(tokens[2])
                self.user_attribute3 = int(tokens[3])
                self.user_attribute4 = int(tokens[4])
                self.user_attribute5 = int(tokens[5])
