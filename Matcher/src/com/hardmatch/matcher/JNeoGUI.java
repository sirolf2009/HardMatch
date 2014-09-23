package com.hardmatch.matcher;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.swing.JButton;
import javax.swing.JEditorPane;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

import org.neo4j.cypher.javacompat.ExecutionEngine;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Label;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.Transaction;

import com.hardmatch.matcher.neo4j.cypher.CypherHelper;
import com.hardmatch.matcher.neo4j.label.LabelSimple;
import com.jgoodies.forms.factories.FormFactory;
import com.jgoodies.forms.layout.ColumnSpec;
import com.jgoodies.forms.layout.FormLayout;
import com.jgoodies.forms.layout.RowSpec;
import javax.swing.JTextPane;

public class JNeoGUI {

	public JFrame frame;
	private JTextField textField;
	private GraphDatabaseService graph;
	private JEditorPane editorPane;
	private JTextArea textArea;
	private JTextField textField_1;
	private ExecutionEngine engine;

	/**
	 * Create the application.
	 * @param graph 
	 */
	public JNeoGUI(GraphDatabaseService graph) {
		this.graph = graph;
		engine = new ExecutionEngine(graph);
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.setBounds(100, 100, 450, 300);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(new FormLayout(new ColumnSpec[] {
				FormFactory.RELATED_GAP_COLSPEC,
				ColumnSpec.decode("default:grow"),
				FormFactory.RELATED_GAP_COLSPEC,
				FormFactory.DEFAULT_COLSPEC,
				FormFactory.RELATED_GAP_COLSPEC,
				FormFactory.DEFAULT_COLSPEC,
				FormFactory.RELATED_GAP_COLSPEC,
				ColumnSpec.decode("default:grow"),},
			new RowSpec[] {
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,
				FormFactory.RELATED_GAP_ROWSPEC,
				RowSpec.decode("default:grow"),}));
		frame.addWindowListener(new CloseDatabase());

		JLabel lblCreateNewNode = new JLabel("Create new node");
		frame.getContentPane().add(lblCreateNewNode, "2, 2");

		JLabel lblBrowseNodes = new JLabel("Browse Nodes");
		frame.getContentPane().add(lblBrowseNodes, "8, 2");

		JLabel lblName = new JLabel("Name");
		frame.getContentPane().add(lblName, "2, 4, right, default");

		textField = new JTextField();
		frame.getContentPane().add(textField, "4, 4, fill, default");
		textField.setColumns(10);

		JButton btnReparse = new JButton("Reparse");
		btnReparse.addActionListener(new ReparseDatabase());
		frame.getContentPane().add(btnReparse, "8, 4");

		JLabel lblProperties = new JLabel("Properties");
		frame.getContentPane().add(lblProperties, "2, 6");

		textArea = new JTextArea();
		frame.getContentPane().add(textArea, "4, 6, fill, fill");

		editorPane = new JEditorPane();
		editorPane.setEditable(false);
		frame.getContentPane().add(editorPane, "8, 6, fill, fill");

		JButton btnCreate = new JButton("Create!");
		btnCreate.addActionListener(new AppendNode());
		frame.getContentPane().add(btnCreate, "2, 8");
		
		JLabel lblSendCypher = new JLabel("Send Cypher");
		frame.getContentPane().add(lblSendCypher, "2, 12");
		
		textField_1 = new JTextField();
		frame.getContentPane().add(textField_1, "2, 14, fill, default");
		textField_1.setColumns(10);
		
		JButton btnSend = new JButton("Send");
		btnSend.addActionListener(new SendCypher());
		frame.getContentPane().add(btnSend, "4, 14");
		
		JTextPane textPane = new JTextPane();
		frame.getContentPane().add(textPane, "2, 16, fill, fill");
	}

	class ReparseDatabase implements ActionListener {

		@Override
		public void actionPerformed(ActionEvent e) {
			Transaction trans = graph.beginTx();
			editorPane.setText("");
			ExecutionEngine engine = new ExecutionEngine(graph);
			for(Node node : CypherHelper.GetAllNodes(engine)) {
				editorPane.setText(editorPane.getText()+"Node ID: "+node.getId()+"\n");
				for(Label label : node.getLabels()) {
					editorPane.setText(editorPane.getText()+"Label: "+label.name()+"\n");
				}
				for(String key: node.getPropertyKeys()) {
					editorPane.setText(editorPane.getText()+"Property("+key+"): "+node.getProperty(key)+"\n");
				}
				for(Relationship relation : node.getRelationships()) {
					editorPane.setText(editorPane.getText()+"Relation: "+relation.getId()+"\n");
					editorPane.setText(editorPane.getText()+"Relation Type: "+relation.getType()+"\n");
				}
				editorPane.setText(editorPane.getText()+"\n");
			}
			trans.close();
		}

	}

	class AppendNode implements ActionListener {

		@Override
		public void actionPerformed(ActionEvent e) {
			String name = textField.getText();
			try(Transaction trans = graph.beginTx()) {
				Node node = graph.createNode(new LabelSimple(name));
				for(String line : textArea.getText().split("\n")) {
					if(line.isEmpty()) {
						continue;
					}
					String propName = line.split(":")[0];
					String propValue = line.split(":")[1];
					node.setProperty(propName, propValue);
				}
				textArea.setText("");
				textField.setText("");
				trans.success();
			}
			new ReparseDatabase().actionPerformed(e);
		}

	}

	class CloseDatabase implements WindowListener {

		@Override
		public void windowActivated(WindowEvent e) {
		}

		@Override
		public void windowClosed(WindowEvent e) {
		}

		@Override
		public void windowClosing(WindowEvent e) {
			Runtime.getRuntime().addShutdownHook(new Thread() {
				@Override
				public void run() {
					graph.shutdown();
				}
			});
		}

		@Override
		public void windowDeactivated(WindowEvent e) {
		}

		@Override
		public void windowDeiconified(WindowEvent e) {
		}

		@Override
		public void windowIconified(WindowEvent e) {
		}

		@Override
		public void windowOpened(WindowEvent e) {
		}

	}
	
	class SendCypher implements ActionListener {

		@Override
		public void actionPerformed(ActionEvent e) {
			String cypher = textField_1.getText();
			CypherHelper.Cypher(engine, cypher);
		}
		
	}

}
