
public class SimpleMapper{

	//Responsiblities: From concept name, acquire products
	// Query db
	//Handle the case of an abstract concept

	public static HashMap<String, Node> lookup;

	//Mongo Driver code here

	public SimpleMapper(HashMap<String, Node> lookup){
		this.lookup = lookup;
	}

	public static ArrayList<Product> queryDb(String concept){
		//query db
		// for each json entry returned, create a product and add it to list
		// return the product list
	}

	public static ArrayList<Product> poll( ArrayList<Product> products){
		//return a list of 3 randomly polled products
		
	}

	public static void main(String args[]){

	}

}
