package fugitivec;

class Person {
    String id;
    String name;
    String sex;
    int age;
    Boolean isFleeing; 
    String desc;

    public Person() {}

    public Person(String id, String name, String sex, int age, Boolean isFlee, String desc) {
        this.id = id;
        this.name = name;
        this.sex = sex;
        this.age = age;
        this.isFleeing = isFlee;
        this.desc = desc;
    }
    public void setID(String id) {
        this.id = id;
    }
    public String getID() {
        return this.id;
    }

    public void setName(String name) {
        this.name = name;
    }
    public String getName() {
        return this.name;
    } 
    public String getSex() {
        return this.sex;
    }
    public int getAge() {
        return this.age;
    }
    public Boolean getIsFleeing() {
        return this.isFleeing;
    }
    public String getDesc() {
        return this.desc;
    }
    public void setDesc(String desc) {
        this.desc = desc;
    }


}


