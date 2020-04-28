import java.util.*;

import java.io.*;

class Node{

	public String name;
	public HashSet<Node> children;
	public HashSet<String> synonyms;	//Is this really needed?
	public Node parent;

	public double confidence;

	public Node(){
		children = new HashSet<>();
		synonyms = new HashSet<>();
		
	}

	public Node(String name, double confidence){
		
		this.name = name;
		this.confidence = confidence;
		children = new HashSet<>();
		synonyms = new HashSet<>();
	}
	
}


public class ConceptHierarchy{

	public static Node root = new Node("Root", 0.1);

	public static HashMap<String,Node> lookup = new HashMap<>();

	public static ArrayList<String> conceptList = new ArrayList<>();

	public static String fileName = "poc-concepts";	//Source file for concept hierarchy

	public static HashMap<String, Node> getConceptHierarchy(){
		return lookup;
	}

	public static void buildConceptHierarchy(){
		lookup.put("Root",root);
		try{
			BufferedReader br = new BufferedReader(new FileReader(new File("poc-concepts")));

			String line;

			String tokens[];

			int lineNumber = 0;			
			while( (line = br.readLine()) != null){
				lineNumber++;
				if(line.startsWith("#") || line.trim().equals("\n")){
					//Line is a comment, ignore
					continue;
				}
				tokens = line.split("\\s");

				if(tokens[0].startsWith("[NewConcept]")){
					Node node = createNode(tokens[1], tokens[2]); //name, score
					if(node == null){
						System.out.println("Error at line: "+ lineNumber + "Node not created. Skipping");
						continue;
					}
					lookup.put(node.name, node);
					conceptList.add(node.name);
				}
				else if(tokens[0].startsWith("[Incoming]")){
					String current = tokens[1];

					Node currentNode = lookup.get(current);
					if(currentNode == null){
						System.out.println("Error at line: " + lineNumber + " node not found!");
						continue;
					}
					
					int n = tokens.length;
					Node currentParent;		
					for(int i = 2; i < n; i++){
						currentParent = lookup.get(tokens[i]);
						if(currentParent == null){
							System.out.println("Error at line: "+ lineNumber+ " " + tokens[i] + " does not exist");
							continue;
						}
						currentParent.children.add(currentNode);
						currentNode.parent = currentParent;		//Links are bidirectional
						System.out.println("Established link between: " + tokens[i] + "->" + current);
					}
				}
				else if(tokens[0].startsWith("[Outgoing]")){
					Node currentParent = lookup.get(tokens[1]);
					if(currentParent == null){
						System.out.println("Error at line: " + lineNumber + " Parent" + tokens[1] + " is not recognized. Skipping.");
						continue;
					}					
					int n = tokens.length;

					Node childNode;
					for(int i = 2; i < n; i++){
						childNode = lookup.get(tokens[i]);
						if(childNode == null){
							System.out.println("Error at line: "+ lineNumber + tokens[i] + " does not exist");
							continue;
						}
						currentParent.children.add(childNode);
						System.out.println("Established link between: " + tokens[i] + "->" + currentParent.name);
						childNode.parent = currentParent;						
					}
				}
				else if(tokens[0].startsWith("[Synonym]")){
					
					int n = tokens.length;

					Node current = lookup.get(tokens[1]);
					for(int i = 2; i < n; i++){
						current.synonyms.add(tokens[i]);
					}
				}
				else{
					System.out.println("Error at line: " + lineNumber + "Invalid file format");
				}

			}
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}

	public static Node createNode(String name, String score){
		Node node = null;		
		try{
			double confidence = Double.parseDouble(score);
			node = new Node(name,confidence);
		}
		catch(Exception e){
			System.out.println("Error in createNode function");
			e.printStackTrace();
		}
		return node;
	}

	public static ArrayList<String> getConceptList(){
		return conceptList;
	}

	public static void displayConcepts(){
		System.out.println(conceptList);
	}

	public static void findSimilarity(String subject1, String subject2){
		Node current1 = lookup.get(subject1);
		Node current2 = lookup.get(subject2);

		Node ancestor = new Node("dummyAncestor", 0.0);

		boolean foundAncestor = false;

		HashSet<Node> current1Path = new HashSet<>();
		HashSet<Node> current2Path = new HashSet<>();

		Node i = current1;

		while(i != null){
			current1Path.add(i);
			i = i.parent;
		}

		i = current2;

		while(i != null){
			current2Path.add(i);
			i = i.parent;
		}

		for(Node n : current1Path){
			if(current2Path.contains(n)){
				if(n.confidence > ancestor.confidence){
					ancestor = n;
				}					
			}
		}

		System.out.println("Ancestor: " + ancestor.name + ", confidence: " + ancestor.confidence);
	}

	// Input: Tag -> list of concept names
	// Output: The concept with highest confidence score
	public static String getConcept(ArrayList<String> conceptNames){
		Node matchedNode = new Node("root", 0.1);
		//Default matchedNode is the root node, with confidence score of 0.1
		Node curr;
		for(String concept : conceptNames){
			curr = lookup.get(concept);
			if(curr == null){
				//Error, skip
				System.out.println("Error, no node with name: " + concept + " exists");
				continue;
			}
			if(matchedNode.confidence < curr.confidence){
				matchedNode = curr;
			}
			
		}
		System.out.println("Best match: " + matchedNode.name);
		return matchedNode.name;
	}

	
	public static void writeLeafNodes(){
		try{
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File("leaf-nodes-descriptor")));

			//Breadth first search on concept hierarchy

			Queue<Node> q = new LinkedList<>();
			q.add(lookup.get("Root"));
			
			Node curr;
			while(!q.isEmpty()){
				curr = q.peek();
				q.remove();
				HashSet<Node> children = curr.children;

				if(children == null){
					continue;
				}
				else if(children.size() == 0){
					String line = getStringPath(curr);
					System.out.println("writing: " + line);
					bw.write(line + "\n");
				}
				else{
					for(Node n : children){
						q.add(n);
					}
				}
			}
			bw.close();

		}
		catch(Exception e){
			e.printStackTrace();
		}
	}

	public static String getStringPath(Node node){
		Node curr = node;
		String path = "";
		
		Node root = lookup.get("Root");
		while(curr != root){
			path = curr.name + " " +path;
			curr = curr.parent;
		}
		return path;
	}

	public static void main(String args[]){
		buildConceptHierarchy();
		findSimilarity("Mobile", "Laptop");
		writeLeafNodes();
	}
}
