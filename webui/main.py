# encoding: utf-8
# all the imports
import os
import sys
import subprocess
from flask import Flask, request, g, redirect, url_for, render_template, flash, session

# from werkzeug import generate_password_hash, check_password_hash
from contextlib import closing
from functools import wraps

# 解决UTF-8编码问题
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'development key'
# MySQL configurations

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_fugitive', methods=['GET', 'POST'])
def add_fugitive():
    if request.method == 'POST':
        
        # 添加逃犯信息
        _id = request.form['add-ID']
        _name = request.form['add-Name']
        _sex = request.form['add-Sex']
        _age = request.form['add-Age']
        _isFugitive = request.form['add-isFugitive']
        _desc = request.form['add-Desc']
        
        cmd = ["java", "-cp", "fugitivec-1.0-SNAPSHOT-jar-with-dependencies.jar", "com.vancir.integration.InvokeChaincode", 
            "add", str(_id), str(_name), str(_sex), str(_age), str(_isFugitive), str(_desc)]

        output = ""
        feedback = ""
        try:
            outputs = subprocess.check_output(cmd)
        except Exception as e:
            print e
        
        output = outputs.split("\n")
        response = ""
        for item in output:
            if item.startswith("Invoke Response:"):
                response = item
                print response
                break

        if response.find("added with") != -1:
            feedback = "成功添加逃犯信息".decode("utf-8") 
        else:
            feedback = "未能成功添加逃犯信息".decode("utf-8") 
    
        return render_template('add_fugitive.html', feedback=feedback)
    return render_template('add_fugitive.html')


@app.route('/delete_fugitive', methods=['GET', 'POST'])
def delete_fugitive():
    if request.method == 'POST':
        # 删除逃犯信息
        _id = request.form['delete-ID']

        cmd = ["java", "-cp", "fugitivec-1.0-SNAPSHOT-jar-with-dependencies.jar", "com.vancir.integration.InvokeChaincode", 
            "delete", str(_id)]

        output = ""
        feedback = ""
        try:
            outputs = subprocess.check_output(cmd)
        except Exception as e:
            print e
        
        output = outputs.split("\n")
        response = ""
        for item in output:
            if item.startswith("Invoke Response:"):
                response = item
                print response
                break

        if response.find("Deleted") != -1:
            feedback = "成功删除逃犯信息".decode("utf-8") 
        else:
            feedback = "未能成功删除逃犯信息".decode("utf-8") 

        return render_template('delete_fugitive.html', feedback=feedback)
    return render_template('delete_fugitive.html')

@app.route('/query_fugitive', methods=['GET', 'POST'])
def query_fugitive():
    if request.method == 'POST':
        # 查询逃犯信息
        _id = request.form['query-ID']

        cmd = ["java", "-cp", "fugitivec-1.0-SNAPSHOT-jar-with-dependencies.jar", "com.vancir.integration.InvokeChaincode", 
            "query", str(_id)]

        output = ""
        feedback = []
        try:
            outputs = subprocess.check_output(cmd)
        except Exception as e:
            print e
        
        output = outputs.split("\n")
        response = ""
        for item in output:
            if item.startswith("Invoke Response:"):
                response = item
                print response
                break

        if response.find("Query Response:") != -1:
            idx = response.find("Query Response:")
            info_string = response[idx+15:]
            attrs = info_string.split(",")
            for item in attrs:
                if item.find("Name:") != -1:
                    _name = item.split(":")[1].strip()
                elif item.find("Sex:") != -1:
                    _sex = item.split(":")[1].strip()
                elif item.find("Age:") != -1:
                    _age = item.split(":")[1].strip()
                elif item.find("isFleeing:") != -1:
                    _isFleeing = item.split(":")[1].strip()
                elif item.find("Description:") != -1:
                    _desc = item.split(":")[1].strip()

            feedback = u"ID: " + _id + "\t" + u"姓名: " + _name + "\t" + u"性别: " + _sex + "\t" + u"年龄: " + _age + "\t" + u"是否已被捉拿: " + _isFleeing + "\n" + u"描述: " + _desc

        else:
            feedback = u"未能成功查询逃犯信息"

        
        return render_template('query_fugitive.html', feedback=feedback)
    return render_template('query_fugitive.html')

@app.route('/update_fugitive', methods=['GET', 'POST'])
def update_fugitive():
    if request.method == 'POST':
        # 修改逃犯描述
        _id = request.form['update-ID']
        _after_desc = request.form['update-Desc']

        cmd = ["java", "-cp", "fugitivec-1.0-SNAPSHOT-jar-with-dependencies.jar", "com.vancir.integration.InvokeChaincode", 
            "update", str(_id), str(_after_desc)]

        output = ""
        feedback = ""
        try:
            outputs = subprocess.check_output(cmd)
        except Exception as e:
            print e
        
        output = outputs.split("\n")
        response = ""
        for item in output:
            if item.startswith("Invoke Response:"):
                response = item
                print response
                break
        
        # Key: %s. Before updated, the message is %s After updated, the message now is %s.
        before_msg_start_idx = response.find("message is") + 10
        before_msg_end_idx = response.find("After")
        before_msg = response[before_msg_start_idx : before_msg_end_idx].strip()

        after_msg_idx = response.find("now is") + 6
        after_msg = response[after_msg_idx:-1]

        feedback = u"修改前的描述: " + before_msg + "\n" + u"修改后的描述: " + after_msg


        return render_template('update_fugitive.html', feedback=feedback)
    return render_template('update_fugitive.html')

if __name__ == '__main__':
    app.run(debug=False, port=5002)