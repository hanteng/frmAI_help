---
tags:
- Cognitive Science
- Relevance
- John McCarthy
- Patrick Hayes
- Large Language Models
---
## Frame Problem 🖼️⏱️ {#sec-frame-problem}

`Frame Problem`, a core challenge to both AI and cognitivie science, investigates how an intelligent being or system, when facing changes in the world, distinguishes "the relevant things that change" from "the irrelevant things that stay the same".  Whether it is a classic **symbolic logic** system or a contemporary **Large Language Model** application, the frame problem must be addressed effectively—otherwise the being or system cannot cope with the complexity and uncertainty of the real world:

> 🖼️⏱️ When the external world (or our understanding of it) changes, what must remain stable?

## ㉄ Right now, what actually matters?

"To meet a myriad of changes with constancy," a Chinese proverb suggests the importance to maintain the constant foundation (frame) to cope with all changes, effectively asking the question:

> *"Right now, what actually matters?"*

At its core, this problem is about how to effectively **"frame" reality** in order to handle the pivotal concept of **"relevance."** In short: how do we consistently respond to changes without losing our unchanging frame

The **Frame Problem** can be divided into roughly two perspectives: the classic perspective identifies the technical bottleneck of formal logic, while the modern one captures the cognitive and situational challenges facing intelligent systems or beings (limited cognitivie resources when facing limitless possibilities).

### 🏛️ 經典觀點：用符號邏輯定義「不變」{#sec-relevance-classic} 

### 🏛️ Classical: Defining "Invariance" with Symbolic Logic {#sec-relevance-classic}

古典觀點起源於 1969 年，由約翰・麥卡錫（John McCarthy）與弗雷德里克・海耶斯（Frederic Hayes）提出，旨在揭示為什麼讓機器人對一個複雜世界的變化進行推理如此困難。他們指出，最直接的邏輯方法（使用框架公理）會導致一個在計算上無法處理的難題——「公理爆炸」。

The classical view originated in 1969, proposed by John McCarthy and Patrick Hayes, aiming to reveal why it is so difficult to get a robot to reason about change in a complex world. They pointed out that the most direct logical approach (using frame axioms) leads to a computationally intractable problem—an "explosion of axioms."

具體用形式邏輯表達世界動態變化時，他們發現，要描述一個行動（如「開燈」）所導致的變化，不僅需要**行動公理**（Action Axioms）來陳述燈會亮，還需要無數條**框架公理**（Frame Axioms）來證明所有其他事物（如房間裡書的位置）都保持不變。這導致了「公理爆炸」的問題，凸顯出單純依賴靜態邏輯來定義世界動態是不可行的。換句話說，機器無法「想太多」。

When expressing the dynamics of the world in formal logic, they found that describing the consequences of an action (such as "turn on the light") requires not only **Action Axioms** to state that the light will turn on, but also countless **Frame Axioms** to prove that everything else (such as the position of a book in the room) remains unchanged. This leads to the problem of "axiom explosion," highlighting that relying purely on static logic to define the dynamics of the world is computationally infeasible. In other words, the machine cannot afford to "think too much."

框架問題經典觀點因此展示了**[符號式人工智慧]()**的計算實現難點，也引導出一些應對的方法，如使用 **環界化**（Circumscription）與 **預設邏輯** （Default Logic）。這些方法在**特定任務或領域**內透過規則和假設進行限縮，有效地迴避了這個問題。然而，這也意謂著以下：

The classical view of the frame problem thus reveals the computational implementation difficulty at the heart of **[symbolic AI]()**, and has also led to some coping mechanisms, such as **Circumscription** and **Default Logic**. These methods effectively sidestep the problem by narrowing things down within a **specific task or domain** using rules and assumptions. However, this also implies the following:

1. **限制範圍**：問題範圍限縮到已知且有限的世界模型。例如，一個已知房間，或一套簡單的機器人任務。

1. **Restricted scope**: The scope of the problem is narrowed to a known, finite world model—for example, a known room, or a simple set of robotic tasks.

2. **明確定義例外**：為避免「公理爆炸」的困境，若不試圖證明所有事物都保持不變，則需明確定義會改變的例外情況。

2. **Explicitly defined exceptions**: To overcome the issue of "axiom explosion," instead of trying to prove that everything remains unchanged, one must explicitly define the exceptional cases that do change.

3. **封閉世界假設**：假設模型中未被明確陳述的資訊都是假的。

3. **Closed-World Assumption**: Assume that any information not explicitly stated in the model is false.


簡言之，框架問題經典觀點表明，在某些「狹窄」的 AI 領域中，框架問題是可控且可被克服的，有效地用符號邏輯定義「不變」及例外。

In short, the classical view of the Frame Problem shows that within certain "narrow" AI domains, the frame problem is manageable and can be overcome, effectively using symbolic logic to define "invariance" and its exceptions.

### 🏙️ 現代觀點：用情境篩選「相關性」{#sec-relevance-modern} 

#### 🏙️ Modern: Filtering "Relevance" through Context {#sec-relevance-modern}

現代觀點源於**認知科學**家對框架問題再詮釋，如丹尼爾・丹內特（Daniel Dennett）與傑瑞・福多（Jerry Fodor），把核心挑戰轉換為深層的「知識論問題」：從海量資訊中，一個智慧系統如何能即時有效地篩選，來完成當前目標而不陷入無止盡的運算迴圈？這問題也引導出，我們如何解釋人類具備的資訊篩選能力：僅憑與當前情境相關的事物做出決策，而無需明確地排除不相關的事物？

The modern view begins from cognitive scientists' reinterpretation of the frame problem—scientists such as Daniel Dennett and Jerry Fodor reframed the core challenge as a deeper "epistemological problem": out of a vast sea of information, how can an intelligent system filter effectively and in real time to accomplish its current goal without falling into an endless computational loop? This question also leads us to ask how we might explain the human capacity for information filtering: making decisions based solely on what is relevant to the current situation, without needing to explicitly rule out everything irrelevant.


在現代人工智慧中，斯圖爾特・羅素（Stuart Russell）與彼得・諾維格（Peter Norvig）等學者也將此挑戰納入考量，他們的著作《人工智慧：現代方法》（1995）推廣**理性代理人**（rational agent）的設計理念，並將框架問題的解決方案從符號邏輯轉向基於**機率與學習**的方法。該教科書介紹如**機率推理**與**貝氏網路**相關方法，並運用最陡下降法（Steepest Descent Method）等最佳化演算法來訓練**強化學習**模型。這些方法讓系統能夠在不確定的世界中，更有效地判斷 **「相關性」** 並做出決策，而不必事先列舉所有不變的事實。

In contemporary artificial intelligence, scholars such as Stuart Russell and Peter Norvig have also incorporated this challenge into their thinking. Their textbook *Artificial Intelligence: A Modern Approach* (1995) popularized the design philosophy of the **rational agent**, shifting the frame problem solution away from symbolic logic and toward methods grounded in **probability and learning**. The textbook introduces methods such as **probabilistic reasoning** and **Bayesian networks**, and uses optimization algorithms such as the **Steepest Descent Method** to train **reinforcement learning** models. These methods allow systems to more effectively judge (or prejudge) **"relevance"** and make decisions in an uncertain world, without having to enumerate every unchanging fact in advance.


在大數據與人工智能成為日常科技賣點的2020年代，肯尼斯・庫基爾（Kenneth Cukier）等人在其著作《Framers》（2021）中，將「框架」概念推向了更廣闊的社會與認知層面。他們主張，在資訊過載的時代，**框架能力**是一種人類獨有的心智優勢，即**選擇與建構**資訊來理解世界，並具備**選擇、改變及創造新框架**的能力。他們認定當代人工智慧雖能處理海量數據、執行判斷，卻難以自主地創造「框架」。

In the 2020s, as big data and artificial intelligence became everyday technological selling points, Kenneth Cukier and his co-authors, in their book *Framers* (2021), pushed the concept of "framing" toward a broader social and technical level. They argued that in an age of information overload, **framing ability** is a uniquely human mental advantage—the capacity to **select and construct** information in order to understand the world, along with the ability to **choose, change, and create new frames**. They concluded that although contemporary AI can process massive amounts of data and execute judgments, it still struggles to autonomously create "frames."


簡言之，框架問題現代觀點表明，不管是機器學習或人類本身，解決框架問題的有具**即時篩選**與**創造適應**的特性。此觀點透過與傳統符號邏輯不同的角度，來**繞過或有效應付**這種**符號式人工智慧**的經典框架問題。

In short, the modern view of the frame problem shows that whether it is machine learning or humans themselves, solving the frame problem requires the traits of **real-time filtering** and **creative adaptation**. This perspective, through a lens quite different from traditional symbolic logic, offers a way to **bypass or effectively cope with** this classical frame problem of **symbolic AI**.

---
## 📌 Implications for AI Practice

**框架問題**是**符號式人工智慧**的核心挑戰，尤其在需要將世界表徵為符號與邏輯規則時。它與**符碼紮根問題**緊密相關：若符號無法有效紮根於現實，其框架便可能無法準確捕捉相關性，進而導致推理錯誤。現代人工智慧不再試圖用窮舉法來解決框架問題，而是透過基於機率的機器學習方法，來應對不確定性並有效管理它。既使有進展，選擇、改變及創造新框架的能力方面，人類仍有優勢。

The **Frame Problem** is a core challenge for **symbolic AI**, particularly wherever the world must be represented using symbols and logical rules. It is closely tied to the **Symbol Grounding Problem**: if symbols cannot be effectively grounded in reality, their frames may fail to accurately capture relevance, leading to reasoning errors. Contemporary AI no longer attempts to solve the frame problem through brute-force enumeration but instead handles and manages uncertainty through probability-based machine-learning methods. Even with this progress, humans still retain an advantage when it comes to selecting, changing, and creating new frames.

### 📦 大型語言模型為例
### 📦 The Case of Large Language Models

大型語言模型（LLMs）的核心運作原理并未根本上解決「經典」框架問題，因為其算力核心並不是「證明」不變真理，而是根據訓練數據「預測」在當前情境下什麼是相關的資訊。

The core operating principle of **Large Language Models (LLMs)** has not fundamentally solved the "classical" frame problem, because their computational core is not about "proving" invariant truths, but about "predicting," based on training data, what is relevant in the current context.

大型語言模型是否真能展現框架問題可解？

Can Large Language Models truly demonstrate that the frame problem has been solved?

### 🥇 奧林匹亞數學競賽
### 🥇 The Mathematical Olympiad

2025 年，儘管新聞頭條聲稱先進的大型語言模型（LLMs）在解決奧林匹亞數學競賽問題上已超越人類，但一項[評估研究](https://arxiv.org/abs/2503.21934)仍顯示，當前的數學導向 LLMs 在嚴格的數學推理任務，特別是推理與證明生成的能力上仍顯不足。

In 2025, although news headlines claimed that advanced Large Language Models (LLMs) had surpassed humans at solving Mathematical Olympiad problems, an [evaluation study](https://arxiv.org/abs/2503.21934) nonetheless showed that current math-oriented LLMs still fall short on rigorous mathematical reasoning tasks—particularly in reasoning and proof-generation ability.

看似矛盾，實則揭示了互補的真相：先進且專注在數學深度思考的大型語言模型能在特定的數學考試情境下表現得像個頂尖學生，但它還不是一個可靠的定理證明生成數學家，特別是在需要多步驟推理和形式嚴謹性情境下。這也間接展示，在面對需要形式嚴謹性與多層次抽象的任務時，單純依賴統計相關性來判斷「相關性」的能力，仍有其本質上的缺陷。

Seemingly contradictory, this in fact reveals a complementary truth: an advanced LLM focused on deep mathematical thinking can perform like a top student on a specific math exam, yet it is still not a reliable theorem-proving mathematician, especially in situations requiring multi-step reasoning and formal rigor. This also indirectly demonstrates that when facing tasks requiring formal rigor and multiple layers of abstraction, relying purely on statistical correlation to judge "relevance" still has an inherent limitation.

這展示了**框架問題**的經典觀點與現代觀點同時有用，讓我們得以更清晰地理解人工智慧在處理 **「相關性」** 時的運作方式。古典觀點告訴我們，在數學證明這種 **「限制範圍」** 的封閉世界中，只要規則被明確定義，框架問題就能**被有效應付或繞過**。在這樣的環境下，LLMs 能夠利用其強大的模式匹配能力，在預設的框架內高效地進行推導。

This shows that both the classical and modern views of the **Frame Problem** are useful at once, allowing us to more clearly understand how artificial intelligence handles **"relevance."** The classical view tells us that in a closed world with a **"restricted scope"**—such as mathematical proof—so long as rules are explicitly defined, the frame problem can be **effectively coped with or bypassed**. In such an environment, LLMs can leverage their powerful pattern-matching capabilities to derive results efficiently within a preset frame.

然而，現代觀點則揭示了 LLMs 的本質性局限。在開放、不確定的真實世界中，「相關性」不再是邏輯公理所能定義的。大型語言模型所展現的看似卓越能力，是已經引導並提示**脈絡**後的**即時篩選**與**創造適應**的特性。它們憑藉統計關聯及脈絡來動態切換框，但這種能力在需要**形式嚴謹**的證明或跳脫統計模式的**深度推理**時便可能失效，生成貌似合理但實則錯誤的內容。

However, the modern view reveals the essential limitations of LLMs. In the open, uncertain real world, "relevance" is no longer something logical axioms can define. The seemingly remarkable ability LLMs display is the trait of **real-time filtering** and **creative adaptation** that has already been guided and primed by **context**. They rely on statistical association and context to dynamically switch frames—but this ability can fail when a task demands **formal rigor** in proof, or **deep reasoning** that departs from statistical patterns, generating content that appears plausible but is in fact wrong.


因此，LLMs 的成功並非解決框架問題，而是以現代觀點的方式，在特定領域用**脈絡**及相關**資識庫**（大量高階數學問題和解法）先進行統計算力進行微調學習的方式，巧妙地**應付**了它。這同時也提醒，**框架問題**仍是核心讓人工智慧應用有效有用的核心技術及哲思問題。

Therefore, the success of LLMs does not represent a solution to the frame problem, but rather, in the manner of the modern view, a clever way of **coping with** it—within a specific domain, using **context** and a related **knowledge base** (a large corpus of advanced math problems and solutions) to first fine-tune with statistical computation. This is also a reminder that the **Frame Problem** remains a core technical and philosophical issue for making AI applications effective and useful.

## 👉接下來
## 👉 Coming Up Next

在理解 意義的「**使用**」的 **框架問題**，與 意義的「**來源**」的 **符碼紮根問題**之後， 接下來：
Having understood the **Frame Problem**, which concerns the "**use**" of meaning, and the **Symbol Grounding Problem**, which concerns the "**source**" of meaning, we turn next to:

* **[完形心理學](01-05-Gestalt_Psychology.zh-hant)** （Gestalt Psychology）介紹人類生存本能擁有的認知捷思的經驗法則，是有什麼樣的**即時篩選**與**創造適應**的特性，同時也有其偏差與偏見。
* **[Gestalt Psychology](01-05-Gestalt_Psychology.en)**, which introduces the rule-of-thumb cognitive shortcuts inherent to human survival instinct—what kind of **real-time filtering** and **creative adaptation** traits they involve, along with their biases and blind spots.

* **[AI 對齊問題](05-02-AI_alignment.zh-hant)**（AI Alignment Problem），這個問題探問 AI 系統的使用目標是否與人類的價值觀一致。
* **[The AI Alignment Problem](05-02-AI_alignment.en)**, which asks whether the goals AI systems are used to pursue align with human values.

## 🪸請參閱
## 🪸 See Also

  - **[第參篇：符號流 AI](03----symbolic_ai.zh-hant) 回應「關聯性爆炸」的工程手法（啟發式、層級化規則、任務約束）與其邊界。
  - **[Part III: Symbolic AI](03----symbolic_ai.en)**: the engineering responses to "relevance explosion" (heuristics, hierarchical rules, task constraints) and their limits.

***

## ✎ 編輯筆記
## ✎ Editorial Notes

- [x] 逐句事實查核 
- [x] 邏輯流程
- [ ] 內部連結－所有相關條目
- [ ] 外部連結－所有相關條目

- [x] Sentence-by-sentence fact check
- [x] Logical flow verification
- [ ] Internal cross-linking (all related entries)
- [ ] External references (all foundational literature)
