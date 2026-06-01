{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red157\green0\blue210;\red45\green45\blue45;\red0\green0\blue0;
\red15\green112\blue1;\red144\green1\blue18;\red0\green0\blue255;\red101\green76\blue29;\red0\green0\blue109;
\red19\green118\blue70;\red32\green108\blue135;}
{\*\expandedcolortbl;;\cssrgb\c68627\c0\c85882;\cssrgb\c23137\c23137\c23137;\cssrgb\c0\c0\c0;
\cssrgb\c0\c50196\c0;\cssrgb\c63922\c8235\c8235;\cssrgb\c0\c0\c100000;\cssrgb\c47451\c36863\c14902;\cssrgb\c0\c6275\c50196;
\cssrgb\c3529\c52549\c34510;\cssrgb\c14902\c49804\c60000;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \expnd0\expndtw0\kerning0
import\cf3  json\cf0 \
\cf2 import\cf3  time\cf0 \
\cf2 import\cf3  random\cf0 \
\cf2 import\cf3  boto3\cf0 \
\cf2 from\cf3  botocore.exceptions \cf2 import\cf3  ClientError\cf0 \
\pard\pardeftab720\partightenfactor0
\cf5 # Initialize DynamoDB table\
\pard\pardeftab720\partightenfactor0
\cf3 dynamodb \cf0 =\cf3  boto3.resource(\cf6 'dynamodb'\cf3 )\cf0 \
\cf3 TABLE_NAME \cf0 = \cf6 "ItemsTable"\cf3 \'a0 \cf5 # Make sure this table exists with primary key 'name'\cf0 \
\cf3 table \cf0 =\cf3  dynamodb.Table(TABLE_NAME)\cf0 \
\pard\pardeftab720\partightenfactor0
\cf7 def \cf8 response\cf3 (\cf9 status_code\cf3 , \cf9 body\cf3 ):\cf0 \
\pard\pardeftab720\partightenfactor0
\cf3 \'a0\'a0\'a0 \cf6 """Helper to return API Gateway\'96compatible responses"""\cf0 \
\cf3 \'a0\'a0\'a0 \cf2 return\cf3  \{\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf6 "statusCode"\cf3 : status_code,\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf6 "headers"\cf3 : \{\cf6 "Content-Type"\cf3 : \cf6 "application/json"\cf3 \},\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf6 "body"\cf3 : json.dumps(body)\cf0 \
\cf3 \'a0\'a0\'a0 \}\
\pard\pardeftab720\partightenfactor0
\cf7 def \cf8 lambda_handler\cf3 (\cf9 event\cf3 , \cf9 context\cf3 ):\cf0 \
\pard\pardeftab720\partightenfactor0
\cf3 \'a0\'a0\'a0 method \cf0 =\cf3  event.get(\cf6 "httpMethod"\cf3 , \cf6 "GET"\cf3 )\cf0 \
\cf3 \'a0\'a0\'a0 path \cf0 =\cf3  event.get(\cf6 "path"\cf3 , \cf6 "/items/l2"\cf3 )\cf0 \
\cf3 \'a0\'a0\'a0 body \cf0 =\cf3  event.get(\cf6 "body"\cf3 ,\cf6 "\cf7 \{\}\cf6 "\cf3 )\cf0 \
\cf3 \'a0\'a0\'a0\
\'a0\'a0\'a0 \cf2 try\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 data \cf0 =\cf3  json.loads(body) \cf2 if\cf3  body \cf2 else\cf3  \{\}\cf0 \
\cf3 \'a0\'a0\'a0 \cf2 except\cf3  json.JSONDecodeError:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 data \cf0 =\cf3  \{\}\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # Root / Health Check\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf2 if\cf3  path \cf0 == \cf6 "/" \cf7 and\cf3  method \cf0 == \cf6 "GET"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "status"\cf3 : \cf6 "ok"\cf3 , \cf6 "message"\cf3 : \cf6 "API is running!"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\
\'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # CRUD Routes using DynamoDB\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf2 if\cf3  path.startswith(\cf6 "/items"\cf3 ):\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 parts \cf0 =\cf3  path.strip(\cf6 "/"\cf3 ).split(\cf6 "/"\cf3 )\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf5 # POST /items\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if \cf8 len\cf3 (parts) \cf0 == \cf10 1 \cf7 and\cf3  method \cf0 == \cf6 "POST"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 name \cf0 =\cf3  data.get(\cf6 "name"\cf3 )\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if \cf7 not\cf3  name:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 400\cf3 , \{\cf6 "error"\cf3 : \cf6 "Name is required"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf5 # Check if item exists\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 try\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 existing \cf0 =\cf3  table.put_item(\cf9 Key\cf0 =\cf3 \{\cf6 "name"\cf3 : name\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 except\cf3  ClientError \cf2 as\cf3  e:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 500\cf3 , \{\cf6 "error"\cf3 : \cf11 str\cf3 (e)\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if \cf6 "Item" \cf7 in\cf3  existing:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 400\cf3 , \{\cf6 "error"\cf3 : \cf6 "Item already exists"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 table.put_item(\cf9 Item\cf0 =\cf3 data)\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "message"\cf3 : \cf6 "Item created"\cf3 , \cf6 "item"\cf3 : data\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf5 # GET / PUT / DELETE /items/\{name\}\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 elif \cf8 len\cf3 (parts) \cf0 == \cf10 2\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 name \cf0 =\cf3  parts[\cf10 1\cf3 ]\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf5 # GET\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if\cf3  method \cf0 == \cf6 "GET"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 try\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 resp \cf0 =\cf3  table.get_item(\cf9 Key\cf0 =\cf3 \{\cf6 "name"\cf3 : name\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 except\cf3  ClientError \cf2 as\cf3  e:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 500\cf3 , \{\cf6 "error"\cf3 : \cf11 str\cf3 (e)\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if \cf6 "Item" \cf7 not in\cf3  resp:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 404\cf3 , \{\cf6 "error"\cf3 : \cf6 "Item not found"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , resp[\cf6 "Item"\cf3 ])\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf5 # PUT\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 elif\cf3  method \cf0 == \cf6 "PUT"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 try\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 existing \cf0 =\cf3  table.get_item(\cf9 Key\cf0 =\cf3 \{\cf6 "name"\cf3 : name\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 except\cf3  ClientError \cf2 as\cf3  e:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 500\cf3 , \{\cf6 "error"\cf3 : \cf11 str\cf3 (e)\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if \cf6 "Item" \cf7 not in\cf3  existing:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 404\cf3 , \{\cf6 "error"\cf3 : \cf6 "Item not found"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 table.put_item(\cf9 Item\cf0 =\cf3 data)\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "message"\cf3 : \cf6 "Item updated"\cf3 , \cf6 "item"\cf3 : data\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf5 # DELETE\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 elif\cf3  method \cf0 == \cf6 "DELETE"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 try\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 existing \cf0 =\cf3  table.get_item(\cf9 Key\cf0 =\cf3 \{\cf6 "name"\cf3 : name\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 except\cf3  ClientError \cf2 as\cf3  e:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 500\cf3 , \{\cf6 "error"\cf3 : \cf11 str\cf3 (e)\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if \cf6 "Item" \cf7 not in\cf3  existing:\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 404\cf3 , \{\cf6 "error"\cf3 : \cf6 "Item not found"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 table.delete_item(\cf9 Key\cf0 =\cf3 \{\cf6 "name"\cf3 : name\})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "message"\cf3 : \cf7 f\cf6 "Item '\cf7 \{\cf3 name\cf7 \}\cf6 ' deleted"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\
\'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # Performance Test Routes\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf2 if\cf3  path \cf0 == \cf6 "/fast" \cf7 and\cf3  method \cf0 == \cf6 "GET"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "status"\cf3 : \cf6 "ok"\cf3 , \cf6 "response_time"\cf3 : \cf6 "fast"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\
\'a0\'a0\'a0 \cf2 if\cf3  path \cf0 == \cf6 "/slow" \cf7 and\cf3  method \cf0 == \cf6 "GET"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 time.sleep(\cf10 2\cf3 )\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "status"\cf3 : \cf6 "ok"\cf3 , \cf6 "response_time"\cf3 : \cf6 "slow (2s)"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\
\'a0\'a0\'a0 \cf2 if\cf3  path \cf0 == \cf6 "/random" \cf7 and\cf3  method \cf0 == \cf6 "GET"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 delay \cf0 =\cf3  random.uniform(\cf10 0.1\cf3 , \cf10 3.0\cf3 )\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 time.sleep(delay)\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "status"\cf3 : \cf6 "ok"\cf3 , \cf6 "response_time"\cf3 : \cf7 f\cf6 "\cf7 \{\cf3 delay\cf7 :.2f\}\cf6 s"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\
\'a0\'a0\'a0 \cf2 if\cf3  path \cf0 == \cf6 "/unstable" \cf7 and\cf3  method \cf0 == \cf6 "GET"\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 if\cf3  random.random() \cf0 < \cf10 0.2\cf3 :\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 500\cf3 , \{\cf6 "error"\cf3 : \cf6 "Random failure occurred"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\'a0\'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 200\cf3 , \{\cf6 "status"\cf3 : \cf6 "ok"\cf3 , \cf6 "message"\cf3 : \cf6 "Request succeeded"\cf3 \})\cf0 \
\cf3 \'a0\'a0\'a0\
\'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # 404 for unrecognized route\cf0 \
\cf3 \'a0\'a0\'a0 \cf5 # ----------------------------------------\cf0 \
\cf3 \'a0\'a0\'a0 \cf2 return\cf3  response(\cf10 404\cf3 , \{\cf6 "error"\cf3 : \cf7 f\cf6 "No route for \cf7 \{\cf3 method\cf7 \} \{\cf3 path\cf7 \}\cf6 "\cf3 \})\cf0 \
}