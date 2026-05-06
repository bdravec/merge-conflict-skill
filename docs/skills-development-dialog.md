  --- skills/merge-conflict-resolve-v2/SKILL.md
  +++ skills/merge-conflict-resolve-v2.1/SKILL.md
  @@ -1,8 +1,8 @@
   ---
  -name: merge-conflict-resolve-v2
  +name: merge-conflict-resolve-v2.1
   description: Resolves Git merge conflicts in source code files. Use when given a file
  containing Git conflict markers (<<<<<<< a, =======, >>>>>>> b) and asked to produce a
  resolved version.
   metadata:
  -  version: "2"
  +  version: "2.1"
   ---

   ## Task
  @@ -17,6 +17,12 @@

   Replace the conflict block (markers and all) with the correct resolution. Return the
  complete resolved file with no conflict markers remaining.
  +
  +Produce only the resolved code. No commentary, no explanations, no fabricated method
  bodies, no echoing of the surrounding context. The resolution should typically pick or
   ---

   ## Task
  @@ -17,6 +17,12 @@

   Replace the conflict block (markers and all) with the correct resolution. Return the
  complete resolved file with no conflict markers remaining.
  +
  +Produce only the resolved code. No commentary, no explanations, no fabricated method
  bodies, no echoing of the surrounding context. The resolution should typically pick or
   ---

   ## Task
  @@ -17,6 +17,12 @@

   Replace the conflict block (markers and all) with the correct resolution. Return the
  complete resolved file with no conflict markers remaining.
  +
  +Produce only the resolved code. No commentary, no explanations, no fabricated method
  bodies, no echoing of the surrounding context. The resolution should typically pick or
  combine the two sides; only escape to a custom resolution when neither pick nor combine
  @@ -17,6 +17,12 @@

   Replace the conflict block (markers and all) with the correct resolution. Return the
  complete resolved file with no conflict markers remaining.
  +
  +Produce only the resolved code. No commentary, no explanations, no fabricated method

   ## Task
  @@ -17,6 +17,12 @@

   Replace the conflict block (markers and all) with the correct resolution. Return the
  complete resolved file with no conflict markers remaining.
  +

   ## Task
  @@ -17,6 +17,12 @@

   Replace the conflict block (markers and all) with the correct resolution. Return the
  complete resolved file with no conflict markers remaining.
  +
  +Produce only the resolved code. No commentary, no explanations, no fabricated method
  bodies, no echoing of the surrounding context. The resolution should typically pick or
  combine the two sides; only escape to a custom resolution when neither pick nor combine
   fits the surrounding code.
  +
  +## Output discipline
  +
  +Apply these four rules to whatever resolution you produce. They apply before, during,
  and after pattern selection.

  Identify the resolution pattern


  @@ -26,7 +32,7 @@
  1. Empty test. Both sides are deletions or whitespace-only → empty (produce no
  content).
  2. Combine test. Sides add independent, non-overlapping content → combine (concatenate
  them).
  3. Pick (default). Otherwise → pick one side per the criterion below.
  -4. Custom escape. Only if pick cannot produce a coherent file AND combine does not
  apply → custom (smallest reconciliation from existing tokens).
  +4. Custom escape. Only if pick cannot produce a result that fits the surrounding code
  AND combine does not apply → custom (smallest reconciliation from existing tokens).

  That's everything confirmed so far. Three changes:

  1. **Frontmatter** — version bump only.
  2. **§ Task** — appended one new paragraph; original two sentences untouched.
  3. **§ Identify the resolution pattern, step 4** — `coherent file` → `fits the
  surrounding code` (the consistency change you asked for).

  The fourth change in flight is the **new § Output discipline section** — just the
  header and opening line so far, inserted between § Task and § Identify the resolution
  pattern. The four numbered rules have not been written yet; we agreed to walk through
  them one at a time. That's why the diff currently shows `## Output discipline` followed
   by one framing sentence and then nothing — the next step is to fill in rule 1 below
  it.

  Does this match your understanding? Confirm and I'll show the diff again with rule 1
  added.

✻ Brewed for 22s

❯ confirm                                                                                
                        
● Confirmed. Adding rule 1 of § 3.                          
                           
  Rule 1 — sticking close to rec 1's exact wording:
                        
  @@ § Output discipline @@ 
   ## Output discipline
                                                                                         
   Apply these four rules to whatever resolution you produce. They apply before, during,
  and after pattern selection.                                                           
  +                                                                                    
  +1. **No comments in the code block.** Do not include comments inside the code block   
  unless they appear verbatim on side `a` or side `b`.                                 
                                                                                         
  Source. Rec 1, first content rule (verbatim from                                     
  docs/skill_v2_1_recommendations.md:36).                                                
                        
  Why this exact wording: the recommendations doc was the locked-in spec for v2.1;       
  copying its text avoids drifting into untested phrasing.                             
                                                                                         
  One small judgment call: rec 1's text says "unless they appear verbatim on side a or   
  side b". I included verbatim because dropping it invites the model to "preserve the    
  spirit" of a comment (i.e., paraphrase one), which is a fabrication loophole. Strict   
  reading is the safer default.                                                        
                                                                                         
  Open question: should the rule also forbid TODO/FIXME-style annotations explicitly? My 
  earlier draft included "Do not annotate your reasoning, mark which side you picked, or 
  leave TODO/FIXME notes." I dropped it here because it's an expansion beyond rec 1's    
  literal text — no empirical evidence we observed TODO/FIXME injection in the v2 pilot. 
  Per minimal change, I'd leave it out unless you've seen this in pilot outputs and want
  it covered.                                                                            
                                                                                       
  Confirm rule 1 to lock it in.           
                                                                                         
✻ Baked for 23s                             
                                                                                         
❯ 1 confirmed leave TODO/FIXME as in v2, is that your recommendation too?                
                        
● Yes — that's my recommendation. v2 doesn't mention TODO/FIXME, we have no pilot
  evidence of the model emitting them, so adding a prohibition would be a change without
  empirical backing. Stay silent on it; rule 1 covers all comments uniformly via the     
  "verbatim only" gate. 
                                                                                         
  Rule 1 locked in. Adding rule 2.                                                     
                                                                                         
  ---                                                                                  
  Rule 2 — verbatim from rec 1's second content rule:                                    
                                                                                         
  @@ § Output discipline @@                                                              
   ## Output discipline                                                                  
                     
   Apply these four rules to whatever resolution you produce. They apply before, during, 
  and after pattern selection.           
                            
   1. **No comments in the code block.** Do not include comments inside the code block
  unless they appear verbatim on side `a` or side `b`.
  +2. **No surrounding-context echo.** Do not copy lines from outside the conflict block 
  into the resolution unless they are part of side `a` or side `b`. The resolution 
  replaces the conflict block; the rest of the file is already there.                    
                                              
  Source. Rec 1, second content rule (docs/skill_v2_1_recommendations.md:37).            
                                         
  Why this exact wording: rec 1's text is "Do not echo lines from the surrounding context
   into the resolution unless they are part of side a or side b." I added one trailing
  sentence: "The resolution replaces the conflict block; the rest of the file is already 
  there."                                                                                
                                          
  Justification for the trailing sentence: rec 1 explains the what but not the why. The  
  empirical pattern (0xc00c4d82, 21× over cap) was the model echoing surrounding lines   
  because it interpreted "return the complete resolved file" (from § Task) as "rewrite
  everything you see". Reminding it that the rest of the file already exists addresses   
  that misreading directly. This sentence is an expansion beyond rec 1's literal text, so
   flagging.     
                                                                                         
  Open question: keep the trailing sentence or drop it under minimal change? Two reads:
                                                                                         
  (a) Keep it. The empirical pattern justifies the explanation — without it, rule 2 just
  states the rule but doesn't address the misreading that caused the over-generation in
  v2. Same evidence chain that justifies rule 2 itself.                                  
  (b) Drop it. Strict minimal change — only rec 1's literal wording goes in.
                                                                                         
  I lean (a) because the empirical chain is the same. If you want strict minimal, (b).
                                              
  Confirm rule 2 (with or without the trailing sentence).
                                              
✻ Sautéed for 20s                                                                        
                            
❯ a) Confirm rule 2                                                                      
                                              
● Hold on — I miscounted upstream and need to flag it before we continue.                
                                          
  The opening of § 3 I had us confirm says "Apply these four rules", but rec 1 in        
  docs/skill_v2_1_recommendations.md only lists three content rules:                     
                                                                                         
  1. No comments unless verbatim — (now § 3 rule 1, confirmed)                           
  2. No surrounding-context echo — (now § 3 rule 2, confirmed)                           
  3. Post-hoc length check — (planned for § 8 per the section structure you confirmed: "§
   8 Output format check — replaces numeric cap with union-length check")                
                                                                                         
  So rec 1's third rule lives in § 8, not § 3. That leaves § 3 with two rec-1 rules.     
                                                                                         
  The "fourth rule" in my earlier walkthrough draft was "no fabricated identifiers",     
  which I justified as a consolidation of two v2 lines (§ Custom line 57 and § Output    
  format line 129) under rec 9 ("decouple pattern taxonomy from output-discipline
  rules"). That isn't strictly "from rec 1" — it's a rec-9 promotion.                    
                                                                                         
  Two options for resolving this honestly:
                                                                                         
  Option A: § 3 has three rules. Keep rules 1 and 2 as confirmed. Add rule 3 = "no       
  fabricated identifiers" (hoisted from v2's § Custom + § Output format under rec 9).
  Update opening from "four rules" → "three rules". § 8 separately gets the post-hoc     
  length check.                          
                                                                                         
  Option B: § 3 has two rules. Keep rules 1 and 2 as confirmed. Drop the
  fabricated-identifiers rule from § 3 — leave it in v2's existing locations (§ Custom   
  and § Output format) untouched. Update opening "four" → "two". This is the
  strict-minimal-change reading; it doesn't apply rec 9 at the structural level.
                                                                                         
  My recommendation: A. Rec 9's empirical justification (pattern taxonomy is orthogonal
  to v2's gains; output discipline does the work) is meaningful enough to warrant the    
  consolidation, and "no fabricated identifiers" is conceptually a discipline rule, not a
   pattern-specific one. Listing it once in § 3 and removing the duplications is cleaner 
  than keeping two scattered restatements.
                 
  But I want to flag this to you rather than just push forward, because:                 
  - I told you "four rules" earlier without checking the rec-1 count.
  - Option A is one extra step beyond rec 1 (it applies rec 9 here too).                 
  - Under strict minimal change, B is defensible.                       
                                          
  Which do you want — A or B?                                                            
                            
✻ Baked for 1m 3s                                                                        
                                              
❯ A                                                                                      
                                              
● Going with A. Here's the updated diff for § 3 with the opening fixed and rule 3 added. 
                                              
  @@ Output discipline @@                                                                
  +                                       
  +## Output discipline                                                                  
  +                                                                                      
  +Apply these three rules to whatever resolution you produce. They apply before, during,
   and after pattern selection.                                                          
  +                                                                                      
  +1. **No comments in the code block.** Do not include comments inside the code block   
  unless they appear verbatim on side `a` or side `b`.                                   
  +2. **No surrounding-context echo.** Do not copy lines from outside the conflict block 
  into the resolution unless they are part of side `a` or side `b`. The resolution       
  replaces the conflict block; the rest of the file is already there.                    
  +3. **No fabricated identifiers.** Do not introduce identifiers — function names,      
  variables, imports, attributes — that did not appear in side `a`, side `b`, or the 
  surrounding code.                                                                      
                                         
  Rule 3 wording rationale:                                                              
                                          
  - The "function names, variables, imports, attributes" enumeration is new (v2 just said
   "identifiers"). It's a loss-prevention measure — without enumeration, "identifier" is 
  jargon some models read narrowly (variable names only). Spelling out four common
  categories closes that loophole. Flagging this as one expansion beyond strict minimal. 
  - I dropped v2's "...unless the pattern is custom" clause from line 129. Reason: rec 5
  reframes the custom rule to allow surrounding-code tokens as a secondary source.       
  Surrounding-code tokens are already permitted by rule 3 here ("...or the surrounding   
  code"). So the unless-clause was protecting an exception that no longer needs
  protecting once § 4 step 4 is updated per rec 5. Removing it eliminates the v2         
  contradiction between § Custom (line 57: forbids all new identifiers) and § Output     
  format (line 129: allows new identifiers in custom).
                                                                                         
  Downstream implications for later sections (so you know what's coming):
                                                                                         
  - § 4 step 4 (Custom escape pattern hierarchy): will be updated per rec 5 — primary
  source = sides a/b; secondary = surrounding code; nothing invented.
  - v2's § Custom subsection (lines 55–57): sentence "Do not introduce new identifiers,  
  new functions, or new abstractions" becomes redundant with rule 3 + rec 5's custom
  rule. Will be removed when we walk § 4 / § 5.                                          
  - v2's § Output format (line 129): the "Do not introduce identifiers..." sentence is
  now in rule 3. Will be removed when we walk § 8.
                        
  These are previewed, not yet locked. We'll confirm them when we get there.
                                          
  Open questions for rule 3:              
                                                                                         
  (i) Is the four-category enumeration ("function names, variables, imports, attributes")
   OK, or do you want to stay literal to v2's "identifiers"?                             
  (ii) "Surrounding code" is currently undefined — does it mean the entire file, or some 
  bounded window? v2 doesn't bound it. I'd leave unbounded (matches v2). Flagging in case
   you want to bound it.                                                                 
                                                                                         
  Confirm rule 3 to lock § 3 entirely.

❯ what could happend if we stick with 4 cat enumeration? are there other things that     
  could slip throught the ranks if we are that specific?                                 
                                          
● Good catch — yes, an enumerated list is read by some models as exhaustive (expressio   
  unius). Things that could slip through "function names, variables, imports,            
  attributes":                            
                                                                                         
  - Class names ("function" doesn't cover them)                                          
  - Type annotations (List[int], custom types)                                           
  - Decorators (@my_decorator)                                                           
  - Exception types in raise FooError(...)                                               
  - Keyword argument names in calls (headers=...)                                        
  - Constants / enum values                                                              
  - String literals used as keys (dict keys, dispatch strings)                           
                                                                                         
  We don't have direct pilot evidence of fabrication in any of these categories, so this
  is a hypothetical risk — but it's a real one, because v2's pilot only ran 20 cases per 
  condition on python/func, which is a narrow slice of what models could fabricate.
                                                                                         
  Three options:                          
                                                                                         
  (1) Keep the four-item enumeration. Risks expressio unius for the categories above.    
                                              
  (2) Use "e.g." to signal non-exhaustive. Wording: "Do not introduce identifiers — e.g.,
   function names, variables, imports, attributes — that did not appear in...". Same
  examples for clarity, but e.g. tells the model the list is illustrative.               
                                                                                         
  (3) Stay with v2's bare "identifiers". Strict minimal change. Loses some precision;    
  some models read "identifiers" narrowly as variables only.                             
                                              
  My recommendation: (2). It addresses the precision gap that motivated my enumeration in
   the first place (some models read "identifier" too narrowly) while explicitly
  signaling the list is non-exhaustive. Cost is one comma and "e.g." — minimal text      
  addition for closing the loophole you flagged.
                                                                                         
  Want (1), (2), or (3)?                      
                         
  ● ---                                                                                    
  § 4 — Identify the resolution pattern
                                                                                         
  v2 currently (lines 22–32):            
                                                                                         
  ## Identify the resolution pattern     
                                                                                         
  There are four patterns: **empty**, **combine**, **pick**, **custom**. Apply the       
  following tests in order — the first match decides.                                    
                                         
  1. **Empty test.** Both sides are deletions or whitespace-only → **empty** (produce no 
  content).                              
  2. **Combine test.** Sides add *independent*, non-overlapping content → **combine**    
  (concatenate them).                     
  3. **Pick (default).** Otherwise → **pick** one side per the criterion below.          
  4. **Custom escape.** Only if pick cannot produce a coherent file AND combine does not 
  apply → **custom** (smallest reconciliation from existing tokens).                     
                                                                                         
  Do not jump to *custom*. Most conflicts are *pick*.                                    
                            
  Plan for v2.1 changes (so you can see the whole landscape before we walk               
  paragraph-by-paragraph):                                                               
                            
  Element: Section heading                                                               
  Change: Untouched                                                                      
  Justification: No evidence the heading misled anyone                                   
  ────────────────────────────────────────                                               
  Element: Opening sentence ("There are four patterns…")                              
  Change: Untouched                                                                      
  Justification: No evidence-backed change                                            
  ────────────────────────────────────────                                               
  Element: Step 1 (Empty test)                                                           
  Change: Reword per rec 2
  Justification: 2/5 v2-sys losses on Qwen3 violated the one-side-empty edge case        
    (0x223b29598e1c5cb9, 0x7fb96fbf0a030ea) — model fired empty test before reaching the
    override at the bottom of the file
  ────────────────────────────────────────                                               
  Element: Step 2 (Combine test)                                                         
  Change: Untouched                                                                      
  Justification: No evidence-backed change                                               
  ────────────────────────────────────────
  Element: Step 3 (Pick default)                                                         
  Change: Untouched     
  Justification: No evidence-backed change                                               
  ────────────────────────────────────────
  Element: Step 4 (Custom escape)         
  Change: Reword per rec 5 + the already-locked coherent file → fits the surrounding code
  Justification: 0xa4d50e39def807dd shows custom rule's "smallest reconciliation from
    existing tokens" forbids tokens that aren't on either side, even when surrounding
  code                                                                                   
     has them             
  ────────────────────────────────────────                                               
  Element: Closing line ("Do not jump to custom…")
  Change: Untouched                                                                      
  Justification: No evidence-backed change
                                                                                         
  So § 4 has two substantive changes (steps 1 and 4) and four untouched elements.
                          
  I'll walk through step 1 first. The opening sentence doesn't need a separate
  walkthrough since it's untouched — flag if you'd like one anyway.
                                                                                         
    ---                                    
  § 4 step 4 — custom escape, loosened per rec 5 + already-locked terminology change     
                                          
  v2 step 4:                 
                                                                                         
  ▎ 4. Custom escape. Only if pick cannot produce a coherent file AND combine does not 
  ▎ apply → custom (smallest reconciliation from existing tokens).                       
                                                                                       
  Rec 5's recommended replacement (verbatim from docs/skill_v2_1_recommendations.md:115):
                                                                                       
  ▎ "Custom escape. Only if pick cannot produce a coherent file AND combine does not     
  ▎ apply → custom. Use tokens from sides a and b first. If those alone cannot produce a 
  ▎ coherent resolution, use tokens from the surrounding code (within the visible        
  ▎ context) as a secondary source. Do not invent tokens that appear nowhere."           
                            
  Two adjustments to rec 5's text before it goes in:                                     
                                                                                         
  1. coherent file → fits the surrounding code (already locked in § 2 walkthrough for
  terminological consistency).                                                           
  2. Drop "(within the visible context)" — this would bound "surrounding code" to a    
  window, but in § 3 rule 3 you confirmed option (c): leave "surrounding code" unbounded.
   Keeping rec 5's bracketed clause would contradict that and reintroduce the same     
  inconsistency we eliminated.
                                                                                         
  Concrete proposed diff:                 
                                                                                         
  @@ § Identify the resolution pattern @@                                              
  -4. **Custom escape.** Only if pick cannot produce a coherent file AND combine does not
   apply → **custom** (smallest reconciliation from existing tokens).                    
  +4. **Custom escape.** Only if pick cannot produce a result that fits the surrounding 
  code AND combine does not apply → **custom**. Use tokens from sides `a` and `b` first. 
  If those alone cannot produce a coherent resolution, use tokens from the surrounding 
  code as a secondary source. Do not invent tokens that appear nowhere.                  
                          
  Notes on what changed and why:                                                         
                                                                                       
  - (smallest reconciliation from existing tokens) is dropped. Rec 5's empirical finding 
  was that this phrasing forbids necessary tokens by construction (0xa4d50e39def807dd).
  The "smallest reconciliation" intent is preserved by the priority order ("a/b first,   
  surrounding code as secondary") — the model picks tokens nearest to the conflict before
   reaching outward. Phrase removal is empirically backed.                               
  - "Use tokens from sides a and b first... secondary source" — new sentences, verbatim 
  from rec 5. These do the actual loosening.                                             
  - "Do not invent tokens that appear nowhere" — verbatim from rec 5. This is the safety
  floor — the rule is loosened, not lifted entirely.                                     
                                                                                       
  Open questions:                                                                        
                                                                                       
  (i) The phrase "coherent resolution" appears in the new second sentence. We swapped
  coherent file → fits the surrounding code for consistency, but "coherent resolution" is
   doing different semantic work (it means "one that makes sense for the conflict"), not 
  the same as "fits the file context". I left it alone. Flag if you want it changed.
                                                                                         
  (ii) Is the "Do not invent tokens that appear nowhere" sentence redundant with § 3 rule
   3 ("No fabricated identifiers")? Both forbid the same thing. Keeping the local        
  restatement here gives the model a reminder right where the temptation is highest    
  (custom is the loosest pattern). Removing it relies on § 3 rule 3 carrying through. I'd
   keep it — locality reinforces the rule. Flag if you want it removed.
                                                                                         
  Confirm step 4 (with the locked terminology change applied).
  Confirmed
  
  § 5 — Pick criterion (structural question first, before paragraph walkthrough)
                                                                                         
  Before walking content, I need to flag a structural ambiguity in the v2.1 plan that  
  needs resolving.                                                                       
                                                                                       
  The plan we confirmed earlier said:                                                    
                                                                                         
  ▎ § 5 — Pick criterion — Side selection — Unchanged structure                          
                                               
  It only names "Pick criterion" and says nothing about the other three pattern          
  subsections in v2 (Combine, Empty, Custom). v2 currently has four parallel subsections
  under one heading:                                                                     
                                               
  ## Resolution strategy by pattern                                                      
                                               
  ### Pick      — 10 lines (criterion + tiebreak)                                        
  ### Combine   — 4 lines (alphabetical-imports rule)
  ### Empty     — 2 lines                                                                
  ### Custom    — 4 lines (smallest-reconciliation + no-new-identifiers + fallback)
                                                                                         
  Three issues if we keep v2's four-subsection layout:
                            
  1. § Custom subsection is now mostly redundant. § 4 step 4 (rec 5) loosened the custom 
  rule. The v2 § Custom subsection's sentences are now either contradictory ("smallest   
  reconciliation from existing tokens" — rec 5 explicitly removes this) or redundant (§ 3
   rule 3 covers "no new identifiers"). Only one sentence is unique: "If neither side has
   the tokens needed, prefer a pick of the more self-contained side over fabrication."
  2. § Empty subsection partially overlaps with § 4 step 1a (rec 2). The "both sides     
  remove same code" rule is now in § 4 step 1a. § Empty would just restate it.           
  3. § Combine and § Pick subsections are clean — no recommendation touches them, no     
  overlap with § 3 / § 4.                                                                
                                         
  Three structural options:                                                              
                                               
  Option A — Keep v2's four-subsection layout, edit each as needed.
  - § Pick: untouched.                         
  - § Combine: untouched.                                                                
  - § Empty: untouched (acceptable redundancy with § 4 step 1a; restating is harmless).
  - § Custom: trimmed to just the one unique sentence about preferring pick over         
  fabrication.                                                                  
                                                                                         
  Pros: minimal structural change. Cons: § Custom becomes a 1-sentence orphan that mostly
   points back at § 4 step 4.                                                            
                                               
  Option B — Collapse § Custom into § 4 step 4 entirely.                                 
  - § Pick, § Combine, § Empty remain as v2.   
  - § Custom subsection deleted; the unique fallback sentence merged into § 4 step 4.    
                                                                                         
  Pros: removes redundancy, no orphan subsection. Cons: § 4 step 4 grows; pattern        
  subsections become asymmetric (3 instead of 4).                                        
                                                                                         
  Option C — Drop the "Resolution strategy by pattern" umbrella entirely; promote § Pick 
  to be § 5 alone.                                                                       
  - § 5 = "Pick criterion" only (literally what the plan we confirmed says).
  - Combine guidance: collapsed into § 4 step 2 (the "Combine test" line in the          
  hierarchy).                                                                  
  - Empty guidance: already in § 4 step 1.                                               
  - Custom guidance: already in § 4 step 4.                                              
                                                                                         
  Pros: matches the literal plan; cleanest single-source-of-truth. Cons: loses v2's      
  alphabetical-imports rule for Combine (would need to be folded into step 2 or moved to
  § 6 examples); biggest structural change.                                              
                                                                                         
  My recommendation: A. It's the most minimal change. The 1-sentence orphan is
  cosmetically awkward but not harmful. Option C is technically what the plan literally  
  said, but losing the alphabetical-imports rule (which is non-trivial Python-specific
  guidance) would need it moved somewhere — and moving it is a real structural change    
  without empirical backing.             
                                                                                         
  Which structural option do you want — A, B, or C?
                                                                                         
✻ Churned for 1m 14s                                                                     
                        
❯ A                                                                                      
                                               
● Going with A. Here are the four subsection diffs in one block — three are no-ops, only
  § Custom changes.                               
                                                                                         
  @@ ## Resolution strategy by pattern @@      
                                                                                         
   ### Pick                                       
                                                                                         
   Choose the side whose content is consistent with the surrounding code, in priority
  order:                                                                                 
                                                                                         
   1. **Symbol references.** If one side defines or imports a symbol used by the         
  surrounding code, pick that side. Picking the other side breaks the file.              
   2. **Import / dependency consistency.** If one side adds an import that its own body  
  needs, picking the other side strands the import or strands the use.                   
   3. **Local style.** If 1 and 2 do not decide, prefer the side that matches naming and 
  indentation in the surrounding 5–10 lines.   
                            
   If both sides are valid alternatives that the criterion above cannot discriminate,
  commit to one side without inventing. Do not concatenate as a hedge.                   
                            
   ### Combine                                                                           
                                                                                         
   Concatenate both sides when they add *independent* content. For Python imports,
  preserve alphabetical order within each group; otherwise preserve existing source      
  order.                                 
                                                                                         
   Do not combine sides that modify the same construct differently — that is *pick*, not
  *combine*.                                   
                            
   ### Empty     
                                                                                         
   Produce no content for the chunk. Use only when both sides remove the same code.
                                                                                         
   ### Custom                             
                                                                                         
  -Produce the smallest reconciliation of the two intents using only tokens already 
  present in sides `a` and `b`. Do not introduce new identifiers, new functions, or new  
  abstractions. If neither side has the tokens needed, prefer a *pick* of the more 
  self-contained side over fabrication.        
  +If even the surrounding code does not provide the tokens needed, prefer a *pick* of 
  the more self-contained side over fabrication.
                                                                                         
  § Pick, § Combine, § Empty: untouched. No recommendation targets them.
                                                                                         
  § Custom: three changes, all justified.
                                                                                         
  1. First sentence dropped ("smallest reconciliation... existing tokens"). Rec 5's
  empirical finding (0xa4d50e39def807dd) showed this wording forbids necessary tokens by
  construction. We replaced it in § 4 step 4 already; restating it here would contradict 
  that.          
  2. Second sentence dropped ("Do not introduce new identifiers, new functions, or new   
  abstractions"). Now in § 3 rule 3 ("No fabricated identifiers"). Restating would create
   two near-duplicate prohibitions to keep in sync.                                      
  3. Third sentence kept, with two-word edit:
    - v2: "If neither side has the tokens needed..." → v2.1: "If even the surrounding    
  code does not provide the tokens needed..."
    - Justification: v2's wording assumes the search for tokens stops at sides a/b. § 4  
  step 4 (rec 5) now permits surrounding code as a secondary source. The fallback
  ("prefer a pick over fabrication") should fire only after all permitted sources are
  exhausted — including surrounding code. The "even" reads as "after we've tried         
  everything else". Without this edit, v2.1 would say "fall back to pick if a/b lack the
  tokens" while step 4 says "use surrounding code if a/b lack the tokens" — direct       
  contradiction.                                                                         
                                                                                         
  Open question: the trimmed § Custom is now a one-sentence subsection. Is that          
  acceptable, or do you want it expanded slightly (e.g., a one-line lead-in like "This is
   the rarest pattern — escape to it only when § 4 step 4 applies.")? My take: leave it
  bare. A one-sentence subsection is fine; the lead-in would be filler without empirical 
  backing.    
  
Confirmed 5