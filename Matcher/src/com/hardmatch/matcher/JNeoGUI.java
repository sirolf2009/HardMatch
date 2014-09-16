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

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Label;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.Transaction;

import com.hardmatch.matcher.neo4j.label.LabelSimple;
import com.jgoodies.forms.factories.FormFactory;
import com.jgoodies.forms.layout.ColumnSpec;
import com.jgoodies.forms.layout.FormLayout;
import com.jgoodies.forms.layout.RowSpec;

public class JNeoGUI {

	public JFrame frame;
	private JTextField textField;
	private GraphDatabaseService graphDb;
	private JEditorPane editorPane;
	private JTextArea textArea;

	/**
	 * Create the application.
	 * @param graphDb 
	 */
	public JNeoGUI(GraphDatabaseService graphDb) {
		this.graphDb = graphDb;
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
				FormFactory.DEFAULT_COLSPEC,
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
				RowSpec.decode("default:grow"),
				FormFactory.RELATED_GAP_ROWSPEC,
				FormFactory.DEFAULT_ROWSPEC,}));
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
	}

	class ReparseDatabase implements ActionListener {

		@Override
		public void actionPerformed(ActionEvent e) {
			Transaction trans = graphDb.beginTx();
			editorPane.setText("");
			for(Node node : graphDb.getAllNodes()) {
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
			try(Transaction trans = graphDb.beginTx()) {
				Node node = graphDb.createNode(new LabelSimple(name));
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
					graphDb.shutdown();
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

}
