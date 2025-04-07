#!/bin/bash

# Define custom IDs for index patterns
# INDEX_PATTERN_NGINX_ID="2f3f7631-1f04-456e-a0fc-98c79b2b5414"
# INDEX_PATTERN_POSTGRES_ID="6bf82cd0-7d34-4c81-ad73-c5db7a7c25e3"
# INDEX_PATTERN_BACKEND_ID="2468baaa-6a32-4b25-a09e-43c6e4eeba32"
# DASHBOARD_ID="eb148107-718e-4f35-93fc-c1a533b2c352"
INDEX_PATTERN_ELK_ID="af3336a1-1fa4-4a6e-a23b-11c7da2b2444"

# Define ILM policy
curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_ilm/policy/logs_policy" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "policy": {
         "phases": {
           "hot": {
             "actions": {
               "rollover": {
                 "max_primary_shard_size": "50GB",
                 "max_age": "30d"
               }
             }
           },
           "warm": {
             "min_age": "30d",
             "actions": {
               "forcemerge": {
                 "max_num_segments": 1
               },
               "shrink": {
                 "number_of_shards": 1
               }
             }
           },
           "cold": {
             "min_age": "90d",
             "actions": {
               "freeze": {}
             }
           },
           "delete": {
             "min_age": "180d",
             "actions": {
               "delete": {}
             }
           }
         }
       }
     }'

# Apply ILM policy to nginx index template
curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_template/nginx_template" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "index_patterns": ["nginx-*"],
       "settings": {
         "number_of_shards": 1,
         "number_of_replicas": 1,
         "index.lifecycle.name": "logs_policy",
         "index.lifecycle.rollover_alias": "nginx"
       }
     }'

# Apply ILM policy to postgres index template
curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_template/postgres_template" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "index_patterns": ["postgres-*"],
       "settings": {
         "number_of_shards": 1,
         "number_of_replicas": 1,
         "index.lifecycle.name": "logs_policy",
         "index.lifecycle.rollover_alias": "postgres"
       }
     }'

# Apply ILM policy to backend index template
curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_template/backend_template" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "index_patterns": ["backend-*"],
       "settings": {
         "number_of_shards": 1,
         "number_of_replicas": 1,
         "index.lifecycle.name": "logs_policy",
         "index.lifecycle.rollover_alias": "backend"
       }
     }'

# Apply ILM policy to elasticsearch index template
curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_template/elasticsearch_template" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "index_patterns": ["elasticsearch-*"],
       "settings": {
         "number_of_shards": 1,
         "number_of_replicas": 1,
         "index.lifecycle.name": "logs_policy",
         "index.lifecycle.rollover_alias": "elasticsearch"
       }
     }'

# Apply ILM policy to kibana index template
curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_template/kibana_template" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "index_patterns": ["kibana-*"],
       "settings": {
         "number_of_shards": 1,
         "number_of_replicas": 1,
         "index.lifecycle.name": "logs_policy",
         "index.lifecycle.rollover_alias": "kibana"
       }
     }'

# Apply ILM policy to logstash index template
curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_template/logstash_template" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "index_patterns": ["logstash-*"],
       "settings": {
         "number_of_shards": 1,
         "number_of_replicas": 1,
         "index.lifecycle.name": "logs_policy",
         "index.lifecycle.rollover_alias": "logstash"
       }
     }'


# Create index pattern for ELK logs
curl --cacert certs/kibana/kibana.crt -X POST "https://kibana:5601/api/saved_objects/index-pattern/${INDEX_PATTERN_ELK_ID}" \
      -H "kbn-xsrf: true" \
      -H "Content-Type: application/json" \
      -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
      -d '{
        "attributes": {
          "title": "elasticsearch-*,kibana-*,logstash-*",
          "timeFieldName": "@timestamp"
        }
      }'



# Create a snapshot repository

curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_snapshot/my_backup" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
       "type": "fs",
       "settings": {
         "location": "/usr/share/elasticsearch/backup/my_backup",
         "compress": true
       }
     }'

# Schedule snapshots

curl -X PUT --cacert /usr/share/logstash/certs/ca/ca.crt "https://es01:9200/_slm/policy/snapshots" \
     -H "Content-Type: application/json" \
     -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
     -d '{
      "name": "snapshot",
      "schedule": "0 0 * * * ?",
      "repository": "my_backup",
      "config": {
        "include_global_state": true,
        "feature_states": []
      },
      "retention": {
        "expire_after": "30d",
        "min_count": 5,
        "max_count": 50
        }
    }'
