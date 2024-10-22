public static void forName(String className) throws ClassNotFoundException
Class.forName("oracle.jdbc.driver.OracleDriver");
public static Connection getConnection(String url) throws SQLException
public static Connection getConnection(String url, Strring name, String password) throws SQLException
Connection con = DriverManager.getConnection("jdbc:oracle:thin:@localhost:1521:xe", "system", "password");
public Statement createStatement() throws SQLException
Statement stmt = con.createStatement();
public ResultSet executeQuery(String sql)throws SQLException  
ResultSet rs=stmt.executeQuery("select * from emp");  
  
while(rs.next()){  
System.out.println(rs.getInt(1)+" "+rs.getString(2));  
}  
public void close()throws SQLException  
con.close();  