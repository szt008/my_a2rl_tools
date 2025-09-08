#!/bin/bash

ros2 topic list | while read topic; do
    echo "\n话题: $topic"
    type=$(ros2 topic info $topic | grep 'Type:' | awk '{print $2}')
    if [ -n "$type" ]; then
        echo "类型: $type"
        ros2 interface show $type
    else
        echo "无法获取类型"
    fi
done
