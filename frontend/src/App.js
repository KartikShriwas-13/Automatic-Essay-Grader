import React, { useState } from "react";
import {
  TextField,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  Container,
  Paper,
  Box,
} from "@mui/material";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [essay, setEssay] = useState("");
  const [grade, setGrade] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:5000/grade", {
        prompt,
        essay,
      });
      setGrade(response.data.score);
      setAnalysis(response.data.analysis);
      setDialogOpen(true);
    } catch (error) {
      console.error("Error grading essay:", error);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 5, borderRadius: 4 }}>
        <Typography variant="h4" gutterBottom>
          ✍️ Automatic Essay Grader
        </Typography>

        <Box mb={3}>
          <TextField
            fullWidth
            label="Enter Essay Prompt"
            variant="outlined"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            multiline
            rows={3}
          />
        </Box>

        <Box mb={3}>
          <TextField
            fullWidth
            label="Enter Your Essay"
            variant="outlined"
            value={essay}
            onChange={(e) => setEssay(e.target.value)}
            multiline
            rows={6}
          />
        </Box>

        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Submit Essay
        </Button>

        <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
          <DialogTitle>📊 Essay Grading Result</DialogTitle>
          <DialogContent>
            <Typography>
              Your essay has been graded! Final Score:{" "}
              <strong>{grade}</strong>
            </Typography>
            {analysis && (
              <Typography mt={2}>
                Word Count: <strong>{analysis.word_count}</strong>
                <br />
                Sentence Count:{" "}
                <strong>{analysis.sentence_count}</strong>
                <br />
                <Typography>
                 Grammar Errors: <strong>{analysis.grammar_issues}</strong>
                 <br />
                 {analysis.grammar_suggestions && analysis.grammar_suggestions.map((issue, index) => (
                   <Typography key={index} variant="body2">• {issue}</Typography>
                  ))}
                 </Typography>

                Prompt Matched:{" "}
                <strong>
                  {analysis.contains_prompt ? "Yes" : "No"}
                </strong>
              </Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDialogOpen(false)}>Close</Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Container>
  );
}

export default App;
